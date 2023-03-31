import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from source.universal.project_types import UserDetails, DatabaseCreate, DatabaseUpdate, DatabaseRemove, StockRequest
cred = credentials.Certificate("stockexchange-fc03e-firebase-adminsdk-16fd9-742b765388.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

def create_user(user_data: UserDetails, password: str) -> DatabaseCreate:
    doc = db.collection("users").document(user_data.id)
    try:
        doc.set({
            "username": user_data.username,
            "email": user_data.email,
            "password": password,
            "portfolio" : {}
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

def change_portfolio(id: str, stock_data: StockRequest):
    doc = db.collection("users").document(id)
    docsnap = doc.get()
    if docsnap.exists:
        try:
            docsnap.get(f"portfolio.{stock_data.company}")
            doc.update({f"portfolio.{stock_data.company}": firestore.Increment(stock_data.shares)})
        except KeyError:
            doc.update({f"portfolio":{stock_data.company: stock_data.shares}})

if __name__ == "__main__":
    pass