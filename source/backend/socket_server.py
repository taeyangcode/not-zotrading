from socketio import Server, WSGIApp
import eventlet

from source.universal.project_types import UserDetails, DatabaseCreate, DatabaseRemove, RegisterError
from source.backend.database import create_user, remove_user

server: Server = Server()
application: WSGIApp = WSGIApp(server)

@server.on("delete_account")
def delete_account(socket_id: str, details: dict[str, str]) -> None:
    print("delete received")
    remove_user(details["id"])

def start_socket_server(port: int | None = None):
    eventlet.wsgi.server(eventlet.listen(("localhost", port or 6000)), application)
