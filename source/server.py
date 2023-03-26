import socketio
import eventlet
from project_types import UserDetails, DatabaseCreate, DatabaseRemove, RegisterError
from database import create_user, remove_user

server: socketio.Server = socketio.Server()
application: socketio.WSGIApp = socketio.WSGIApp(server)

@server.on("register")
def register(socket_id: str, details: dict[str, str]) -> None | RegisterError:
    create_result = create_user(UserDetails(details["username"], details["email"], details["password"], details["id"]))
    if create_result == DatabaseCreate.CreateFailure:
        return RegisterError.UnexpectedError
    return None

@server.on("delete_account")
def delete_account(socket_id: str, details: dict[str, str]) -> None:
    print("delete received")
    remove_user(details["id"])
    # if result == DatabaseRemove.RemoveSuccess:
    #     return "Deleted"
    # else:
    #     return "Failed to delete"


eventlet.wsgi.server(eventlet.listen(("localhost", 3000)), application)
