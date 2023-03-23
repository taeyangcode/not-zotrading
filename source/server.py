import socketio
import eventlet
from database import create_user
from types import UserDetails



server: socketio.Server = socketio.Server()
application: socketio.WSGIApp = socketio.WSGIApp(server)

eventlet.wsgi.server(eventlet.listen(("", 3000)), server)

@server.event
def register(data: UserDetails) -> None:
    create_user(data)
    
