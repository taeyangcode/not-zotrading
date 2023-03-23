import socketio
import eventlet
import source.types
import source.database

server: socketio.Server = socketio.Server()
application: socketio.WSGIApp = socketio.WSGIApp(server)

@server.event
def register(socket_id: str, details: dict[str, str]) -> None:
    source.database.create_user(source.types.UserDetails(details["username"], details["email"], details["password"], details["id"]))

eventlet.wsgi.server(eventlet.listen(("localhost", 3000)), application)
