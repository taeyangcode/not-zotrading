from threading import Thread
from flask import Flask

from source.backend.server import HTTPServer
from source.backend.socket_server import start_socket_server

flask_server = Flask(__name__)
def start_http_server() -> None:
    HTTPServer(flask_server)

http_server_thread = Thread(target = start_http_server)
http_server_thread.start()

socket_server_thread = Thread(target = start_socket_server)
socket_server_thread.start()
