import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from project_types import UserDetails, DatabaseCreate, DatabaseUpdate, DatabaseRemove
cred = credentials.Certificate("stockexchange-fc03e-firebase-adminsdk-16fd9-742b765388.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()


def create_user(user_data: UserDetails) -> DatabaseCreate:
    doc = db.collection("users").document(user_data.id)
    try:
        doc.set({
            "username" : user_data.username,
            "email" : user_data.email,
            "password" : user_data.password
        })
        return DatabaseCreate.CreateSuccess
    except:
        return DatabaseCreate.CreateFailure

def read_user(id: str) -> dict:
    doc_ref = db.collection("users").document(id)
    doc = doc_ref.get()
    return doc.to_dict()

def update_user(id: str, new_data: dict) -> DatabaseUpdate:
    doc = db.collection("users").document(id)
    if doc.get().exists:
        doc.update(new_data)
        return DatabaseUpdate.UpdateSuccess
    else:
        return DatabaseUpdate.UpdateFailure

def remove_user(id: str) -> DatabaseRemove:
    print("deleting")
    doc = db.collection("users").document(id)
    docsnap = doc.get()
    if docsnap.exists:
        fields = docsnap.to_dict().keys()
        for field in fields:
            doc.update({
                field : firestore.DELETE_FIELD
            })
        doc.delete()
        return DatabaseRemove.RemoveSuccess
    else:
        return DatabaseRemove.RemoveFailure

if __name__ == "__main__":
    pass
