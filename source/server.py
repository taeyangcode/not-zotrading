import socketio
import eventlet
import source.types
import source.database

server: socketio.Server = socketio.Server()
application: socketio.WSGIApp = socketio.WSGIApp(server)

eventlet.wsgi.server(eventlet.listen(("", 3000)), server)

@server.event
def register(data: source.types.UserDetails) -> None:
    print(data)
    source.database.create_user(data)
