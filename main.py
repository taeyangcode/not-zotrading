from source.client import client, Guest, User

user: Guest = Guest(client)
user.register("username", "email", "password")
