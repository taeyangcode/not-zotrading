import socketio
import eventlet

server: socketio.Server = socketio.Server()
application = socketio.WSGIApp(server)

eventlet.wsgi.server(eventlet.listen(("", 3000)), server)
