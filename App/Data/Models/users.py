from App.Data import Document, db


class User(Document):
    collection = db.users
