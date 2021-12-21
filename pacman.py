#!/usr/bin/env python3
"""PACManager, a naive pipeline manager."""
import fileinput
import json
import argparse
import http.server
import traceback

from io import BytesIO


def getProjects(data: dict):
    """Extract the project from the status."""
    return data["DONE"], data["DOING"], data["TODO"], data["PENDING"]


def updateData(data: dict, todo: dict):
    """Safely update data from todo."""
    output = data.copy()
    updating = todo.copy()
    for k, v in updating.items():
        output["TODO"][k] = v
        output["PENDING"].pop(k, None)
    return output


def pacmain(data: dict):
    """Update data if compilation is needed."""
    done, doing, todo, pending = getProjects(data)
    for key, project in pending.items():
        # filter pending dependencies
        # dont care about external dependencies
        pending_dependencies = [i for i in project.get("dependencies")
                                if i in pending.keys()
                                or i in doing.keys()
                                or i in todo.keys()]
        if len(pending_dependencies) == 0:
            todo[key] = project.copy()

    return updateData(data, todo)


###############################################################################
# Server Mode
###############################################################################
# https://blog.anvileight.com/posts/simple-python-http-server/

class Handler(http.server.BaseHTTPRequestHandler):
    """
    The most simple and bare http requests handler.

    Expose Pacmain function on the web.
    """

    def do_GET(self):
        """Respond to GET requests."""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Use POST to send data.')

    def do_POST(self):
        """Respond to POST requests."""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        try:
            data = pacmain(json.loads(body.decode("utf8")))
            self.send_response(200)
            self.end_headers()
            response.write(json.dumps(data).encode())
            self.wfile.write(response.getvalue())
        except KeyError as e:
            self.send_response(500,
                               f"Cannot process input: {e}")

            response.write(traceback.format_exc().encode())
            self.wfile.write(response.getvalue())
            self.end_headers()


def serverMode(host, port):
    """Instanciate a simple http server."""
    print(f"Serving at: http://{host}:{port}")
    httpd = http.server.HTTPServer((host, port), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PACManager, '
                                     'solve your pipeline dependecy tree.')
    parser.add_argument('--server', help="Enable server mode.",
                        action="store_true", required=False)
    parser.add_argument('--port', type=int,
                        help="Change the port.",
                        default=8000,
                        required=False)
    parser.add_argument('--address', type=str, help="Change the adress.",
                        default='0.0.0.0',
                        required=False)
    parser.add_argument('inputfile', type=str,
                        help="the file path if there is no sever mode",
                        nargs='?')
    args = parser.parse_args()
    if args.server:
        serverMode(args.address, args.port)
    else:
        # Read file or stdin
        # https://stackoverflow.com/questions/1744989/read-from-file-or-stdin
        INPUT_FILE = ""
        for line in fileinput.input(args.inputfile):
            INPUT_FILE += str(line)
        INPUT_DATA = json.loads(INPUT_FILE)
        OUTPUT_DATA = pacmain(INPUT_DATA)
        print(json.dumps(OUTPUT_DATA))
