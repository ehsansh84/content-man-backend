from dotenv import load_dotenv
import os
load_dotenv()


def db():
    from pymongo import MongoClient
    con = MongoClient(Settings.MONGO_URL)
    return con[Settings.DB_NAME]


def get_hash(string: str) -> str:
    import hashlib
    text_encoded = string.encode('utf-8')
    hashed_text = hashlib.sha256(text_encoded).hexdigest()
    return hashed_text


class Settings:
    MONGO_URL = os.environ.get('MONGO_URL')
    PROJECT_PATH = os.environ.get('PROJECT_PATH')
    DB_NAME = os.environ.get('DB_NAME')
