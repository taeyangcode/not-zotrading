import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import source.types
cred = credentials.Certificate("stockexchange-fc03e-firebase-adminsdk-16fd9-742b765388.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()


def create_user(user_data: source.types.UserDetails) -> None:
    doc = db.collection("users").document(user_data.id)
    doc.set({
        "username" : user_data.username,
        "email" : user_data.email,
        "password" : user_data.password
    })

def read_user(id: str) -> dict:
    doc_ref = db.collection("users").document(id)
    doc = doc_ref.get()
    return doc.to_dict()

def update_user(id: str, new_data: dict) -> source.types.DatabaseUpdate:
    doc = db.collection("users").document(id)
    if doc.get().exists:
        doc.update(new_data)
        return source.types.DatabaseUpdate.UpdateSuccess
    else:
        return source.types.DatabaseUpdate.UpdateFailure

def remove_user(id: str) -> source.types.DatabaseRemove:
    doc = db.collection("users").document(id)
    if doc.get().exists:
        doc.delete()
        return source.types.DatabaseRemove.RemoveSuccess
    else:
        return source.types.DatabaseRemove.RemoveFailure

if __name__ == "__main__":
    pass
