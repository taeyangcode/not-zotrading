from threading import Thread
from time import sleep
from flask import Flask
from socketio import Client
from requests import post

from source.frontend.client import create_client_connection, Guest, User

from source.backend.server import HTTPServer
from source.backend.socket_server import start_socket_server

flask_server = Flask(__name__)
def start_http_server() -> None:
    HTTPServer(flask_server)

http_server_thread = Thread(target = start_http_server)
http_server_thread.start()

socket_server_thread = Thread(target = start_socket_server)
socket_server_thread.start()

def create_user() -> None:
    sleep(3)
    user: Guest = Guest(create_client_connection(Client()))
    user.register("username_1", "email_1", "password_1", "id_1")
user_thread = Thread(target = create_user)
user_thread.start()
