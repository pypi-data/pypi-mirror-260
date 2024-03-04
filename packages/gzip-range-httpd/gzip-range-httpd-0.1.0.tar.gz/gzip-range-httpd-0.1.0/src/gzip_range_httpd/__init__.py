"""
Use this in the same way as Python's SimpleHTTPServer:

  python -m RangeHTTPServer [port]

The only difference from SimpleHTTPServer is that RangeHTTPServer supports
'Range:' headers to load portions of files. This is helpful for doing local web
development with genomic data files, which tend to be to large to load into the
browser all at once.
"""

import io
from pathlib import Path
import re
from http.server import SimpleHTTPRequestHandler
from typing import Optional

__version__ = "0.1.0"


def copy_byte_range(
    infile, outfile, start=None, stop=None, bufsize=16 * 1024, encoding="gzip"
):
    """Like shutil.copyfileobj, but only copy a range of the streams.

    Both start and stop are inclusive.
    """
    byte_stream = io.BytesIO()

    if start is not None:
        infile.seek(start)
    while 1:
        to_read = min(bufsize, stop + 1 - infile.tell() if stop else bufsize)
        buf = infile.read(to_read)
        if not buf:
            break
        byte_stream.write(buf)

    if encoding == "gzip":
        import gzip

        compressed = gzip.compress(byte_stream.getvalue())
    elif encoding == "zlib":
        import zlib

        compressed = zlib.compress(byte_stream.getvalue())
        buf = byte_stream.read()
        outfile.write(zlib.decompress(buf))
    elif encoding == "deflate":
        compressed = byte_stream.getvalue()

    outfile.write(compressed)


BYTE_RANGE_RE = re.compile(r"bytes=(\d+)-(\d+)?$")


def parse_byte_range(byte_range):
    """Returns the two numbers in 'bytes=123-456' or throws ValueError.

    The last number or both numbers may be None.
    """
    if byte_range.strip() == "":
        return None, None

    m = BYTE_RANGE_RE.match(byte_range)
    if not m:
        raise ValueError("Invalid byte range %s" % byte_range)

    first, last = [x and int(x) for x in m.groups()]
    if last and last < first:
        raise ValueError("Invalid byte range %s" % byte_range)
    return first, last


class GzipRangeRequestHandler(SimpleHTTPRequestHandler):
    """Adds support for HTTP 'Range' requests to SimpleHTTPRequestHandler

    The approach is to:
    - Override send_head to look for 'Range' and respond appropriately.
    - Override copyfile to only transmit a range when requested.
    """

    max_file_size: Optional[int] = None
    encoding: str = "gzip"

    def __init__(self, *args, **kwargs):
        self.range = None
        super().__init__(*args, **kwargs)

    def send_head(self):

        path = Path(self.translate_path(self.path))
        if not path.exists():
            self.send_error(404, "File not found")
            return None

        if path.is_dir():
            return SimpleHTTPRequestHandler.send_head(self)

        file_len = path.stat().st_size
        last_modified = self.date_time_string(path.stat().st_mtime)

        if self.max_file_size is None and "Range" not in self.headers:
            self.range = None
            return SimpleHTTPRequestHandler.send_head(self)

        if "Range" in self.headers:
            try:
                self.range = parse_byte_range(self.headers["Range"])
            except ValueError:
                self.send_error(400, "Invalid byte range")
                return None
        else:
            if file_len < self.max_file_size:
                # File is small enough to send all at once
                return SimpleHTTPRequestHandler.send_head(self)

            self.range = (0, self.max_file_size - 1)

        first, last = self.range

        if first >= file_len:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        ctype = self.guess_type(path)

        try:
            f = open(path, "rb")
        except IOError:
            self.send_error(404, "File not found")
            return None

        self.send_response(206)
        self.send_header("Content-type", ctype)

        if last is None or last >= file_len:
            last = file_len - 1
        response_length = last - first + 1

        content = io.BytesIO()

        copy_byte_range(f, content, start=first, stop=last, encoding=self.encoding)

        f.close()

        response_length = max(response_length, len(content.getvalue()))

        self.send_header("Content-Range", "bytes %s-%s/%s" % (first, last, file_len))
        self.send_header("Content-Encoding", self.encoding)
        # self.send_header("Transfer-Encoding", self.encoding)

        self.send_header("Content-Length", str(response_length))
        self.send_header("Last-Modified", last_modified)
        self.end_headers()

        content.seek(0)
        return content

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        return SimpleHTTPRequestHandler.end_headers(self)

    # def copyfile(self, source, outputfile):
    #     if not self.range:
    #         return SimpleHTTPRequestHandler.copyfile(self, source, outputfile)

    #     # SimpleHTTPRequestHandler uses shutil.copyfileobj, which doesn't let
    #     # you stop the copying before the end of the file.
    #     start, stop = self.range  # set in send_head()
    #     copy_byte_range(source, outputfile, start, stop, encoding=self.encoding)
