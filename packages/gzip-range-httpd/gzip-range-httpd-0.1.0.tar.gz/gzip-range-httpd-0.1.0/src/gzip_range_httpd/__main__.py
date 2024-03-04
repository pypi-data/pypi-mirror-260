"""
Use this in the same way as Python's SimpleHTTPServer:

  python -m gzip_range_httpd [port]

The only difference from SimpleHTTPServer is that RangeHTTPServer supports
'Range:' headers to load portions of files. This is helpful for doing local web
development with genomic data files, which tend to be to large to load into the
browser all at once.
"""

import contextlib
import os
import http.server as SimpleHTTPServer
import socket


from . import GzipRangeRequestHandler

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "port",
    action="store",
    default=8000,
    type=int,
    nargs="?",
    help="Specify alternate port [default: 8000]",
)
parser.add_argument(
    "--max-file-size",
    action="store",
    type=int,
    help="Specify the maximum file size to serve without serving it as a range. [default: None]",
)

parser.add_argument(
    "--encoding",
    choices=["gzip", "zlib", "deflate"],
    default="gzip",
    help="Specify the encoding to use for serving files. [default: gzip]",
)

parser.add_argument(
    "-d",
    "--directory",
    default=os.getcwd(),
    help="serve this directory " "(default: current directory)",
)

args = parser.parse_args()

if args.max_file_size is not None:
    GzipRangeRequestHandler.max_file_size = args.max_file_size

if args.encoding is not None:
    GzipRangeRequestHandler.encoding = args.encoding


# ensure dual-stack is not disabled; ref #38907
class DualStackServer(SimpleHTTPServer.ThreadingHTTPServer):

    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(
            request, client_address, self, directory=args.directory
        )


SimpleHTTPServer.test(
    ServerClass=DualStackServer,
    HandlerClass=GzipRangeRequestHandler,
    port=args.port,
)
