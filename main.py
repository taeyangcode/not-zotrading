from source.client import client, Guest, User

# should create a user and then delete it right after
user: Guest = Guest(client)
# user.id = "6fbbbad6-732f-4908-90d1-9533c45ed6d0"
user.register("username", "email", "password")
user.delete_account()
# print(user.id)
print("this doesnt work without this print statment because of async i think")
user.disconnect()