from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "0.0.0.0"
PORT = 8000


class JarvisHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "status": "online",
                "message": "JARVIS backend is running"
            })
        else:
            self.send_json(404, {
                "error": "Not found"
            })

    def do_POST(self):
        if self.path != "/chat":
            self.send_json(404, {
                "error": "Not found"
            })
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            data = json.loads(body.decode("utf-8"))
            message = data.get("message", "").strip()

            if not message:
                self.send_json(400, {
                    "error": "Message is empty"
                })
                return

            # Temporary response.
            # Real AI connection will be added next.
            reply = (
                "JARVIS received your message: "
                + message
            )

            self.send_json(200, {
                "reply": reply
            })

        except Exception as e:
            self.send_json(500, {
                "error": str(e)
            })


if __name__ == "__main__":
    print("================================")
    print(" J.A.R.V.I.S BACKEND ONLINE")
    print("================================")
    print("Server: http://127.0.0.1:8000")

    server = HTTPServer((HOST, PORT), JarvisHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nJARVIS backend stopped.")
        server.server_close()

