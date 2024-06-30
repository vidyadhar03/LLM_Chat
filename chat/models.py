from pymongo import MongoClient
import certifi
from django.conf import settings

client = MongoClient(
    settings.MONGO_URI,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True
)
db = client[settings.MONGO_DB_NAME]

class UserChats:
    collection = db.user_chat

    @staticmethod
    def create(username):
        if not UserChats.collection.find_one({"username": username}):
            UserChats.collection.insert_one({"username": username, "sessions": []})

    @staticmethod
    def get(username):
        return UserChats.collection.find_one({"username": username})

    @staticmethod
    def add_session(username, model_name):
        UserChats.collection.update_one(
            {"username": username},
            {"$push": {"sessions": {"model": model_name, "messages": []}}}
        )

    @staticmethod
    def add_message(username, model_name, role, content):
        UserChats.collection.update_one(
            {"username": username, "sessions.model": model_name},
            {"$push": {"sessions.$.messages": {"role": role, "content": content}}}
        )
