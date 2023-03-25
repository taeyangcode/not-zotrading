from socketio import Client
from source.client import create_client_connection, Guest, User

# should create a user and then delete it right after
user: Guest = Guest(Client())
# user.id = "6fbbbad6-732f-4908-90d1-9533c45ed6d0"
user = user.register("username", "email", "password")
if type(user) is User:
    print("user has been registered")
    user.delete_account()
    print(user.id)
else:
    print("user could not be registered")
    exit(0)
user.client.disconnect();
