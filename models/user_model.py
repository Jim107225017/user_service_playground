from mongoengine import Document, StringField, connect

# Connect to MongoDB
MONGO_DB = "user_service_playground"
client = connect(db=MONGO_DB)


class User(Document):
    name = StringField(required=True, unique=True, min_length=3, max_length=32)
    password = StringField(required=True, min_length=64, max_length=64)
    salt = StringField(required=True, min_length=64, max_length=64)  # For password hashing
    
    meta = {"collection": "users"}
