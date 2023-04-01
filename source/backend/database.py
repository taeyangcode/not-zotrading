import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from returns.result import Success, Failure, Result
from source.universal.project_types import UserDetails, DatabaseError, StockRequest

cred = credentials.Certificate("stockexchange-fc03e-firebase-adminsdk-16fd9-742b765388.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

def create_user(user_data: UserDetails, password: str) -> Result[(), DatabaseError]:
    doc = db.collection("users").document(user_data.id)
    try:
        doc.set({
            "username": user_data.username,
            "email": user_data.email,
            "password": password,
            "portfolio" : {}
        })
        return Success(())
    except:
        return Failure(DatabaseError.UnexpectedError)

def read_user(id: str) -> Result[dict[str, str], DatabaseError]:
    doc_ref = db.collection("users").document(id)
    doc = doc_ref.get()
    if doc.exists:
        return Success(doc.to_dict())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def update_user(id: str, new_data: dict) -> Result[(), DatabaseError]:
    doc = db.collection("users").document(id)
    if doc.get().exists:
        doc.update(new_data)
        return Success(())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def remove_user(id: str) -> Result[(), DatabaseError]:
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
        return Success(())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def change_portfolio(id: str, stock_data: StockRequest) -> None:
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
