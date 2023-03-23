import socketio
import eventlet
from project_types import UserDetails
from database import create_user

server: socketio.Server = socketio.Server()
application: socketio.WSGIApp = socketio.WSGIApp(server)

@server.event
def register(socket_id: str, details: dict[str, str]) -> None:
    create_user(UserDetails(details["username"], details["email"], details["password"], details["id"]))

eventlet.wsgi.server(eventlet.listen(("localhost", 3000)), application)
