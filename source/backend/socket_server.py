from socketio import Server, WSGIApp
import eventlet

server: Server = Server()
application: WSGIApp = WSGIApp(server)

def start_socket_server(port: int | None = None):
    eventlet.wsgi.server(eventlet.listen(("localhost", port or 6000)), application)
