import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from returns.result import Success, Failure, Result
from source.universal.project_types import UserDetails, DatabaseError, StockRequest

cred = credentials.Certificate("stockexchange-fc03e-firebase-adminsdk-16fd9-742b765388.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

def create_user(user_data: UserDetails, password: str) -> Result[(), DatabaseError]:
    user_data_dict: dict[str, str] = user_data.to_dict()
    doc_ref = db.collection("users").document(user_data_dict["id"])
    if doc_ref.get().exists:
        return Failure(DatabaseError.UserAlreadyExists)
    try:
        doc_ref.set(user_data_dict)
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
    doc_ref = db.collection("users").document(id)
    if doc_ref.get().exists:
        doc_ref.update(new_data)
        return Success(())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def remove_user(id: str) -> Result[(), DatabaseError]:
    print("deleting")
    doc_ref = db.collection("users").document(id)
    docsnap = doc_ref.get()
    if docsnap.exists:
        fields = docsnap.to_dict().keys()
        for field in fields:
            doc_ref.update({
                field : firestore.DELETE_FIELD
            })
        doc_ref.delete()
        return Success(())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def change_portfolio(id: str, stock_data: StockRequest) -> None:
    doc_ref = db.collection("users").document(id)
    docsnap = doc_ref.get()
    if docsnap.exists:
        try:
            docsnap.get(f"portfolio.{stock_data.company}")
            doc_ref.update({f"portfolio.{stock_data.company}": firestore.Increment(stock_data.shares)})
        except KeyError:
            doc_ref.update({f"portfolio":{stock_data.company: stock_data.shares}})
        return Success(())
    else:
        return Failure(DatabaseError.UserDoesNotExist)

def _add_company(company: str, price: int) -> Result[(), DatabaseError]:
    doc_ref = db.collection("stocks").document(company)
    try:
        doc_ref.set({
            "price" : price
        })
        return Success(())
    except:
        return Failure(DatabaseError.UnexpectedError)

def get_stock_price(company: str) -> Result[int, DatabaseError]:
    doc_ref = db.collection("stocks").document(company)
    docsnap = doc_ref.get()
    if docsnap.exists:
        return Success(docsnap["price"])
    else:
        return Failure(DatabaseError.CompanyDoesNotExist)

if __name__ == "__main__":
    pass
