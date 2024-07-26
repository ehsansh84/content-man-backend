from datetime import datetime
from bson import ObjectId
import os
module_dir = os.path.dirname(os.path.abspath(__file__))
from publics import db as database
from typing import List
from app.tools.log_tools import logger_exceptions
reserved_words = ['db', 'col', 'module_name', 'module_text']


class DB:
    f"""
    Use this model to manage an entity
    """

    def to_json(self) -> dict:
        result = {}
        for k, v in vars(self).items():
            if not k.startswith('_DB__'):
                if k not in reserved_words:
                    result[k] = v
            if k == '_id':
                if v in ['', None]:
                    del result['_id']
                else:
                    result['id'] = v
        return result

    @staticmethod
    def serialize_dict(data: dict) -> dict:
        result = {}
        for k, v in data.items():
            if k == '_id':
                if v in ['', None]:
                    continue
                else:
                    result['id'] = str(v)
            else:
                result[k] = v
        return result

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    @classmethod
    def serialize_list(cls, data):
        return [cls.serialize_dict(item) for item in data]

    def __init__(self, _id='', module_name=None, module_text=None, db=None):
        self.module_name = module_name
        self.module_text = module_text
        self.created_at = ''
        self.updated_at = ''
        self._id: str = _id
        self.db = db if db is not None else database()
        self.col = self.db[module_name]
        self.__loaded = False
        if self.check_id_supplied():
            self.load()

    def get_nullable_fields(self):
        try:
            from typing import get_type_hints
            return [k for k in get_type_hints(type(self)).items() if k in vars(self)]
        except KeyError as e:
            logger_exceptions.error(e)

    def check_id_supplied(self):
        return not (self._id is None or self._id == '')

    def load_result(self, result):
        try:
            for key, value in result.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        except KeyError as e:
            logger_exceptions.error(e)

    def before_insert(self):
        pass

    def before_update(self):
        pass

    def prepare_insert(self) -> dict:
        if self._id is not None:
            raise ValueError("This class is loaded, so it can not be inserted")
        self.before_insert()
        self.created_at = self.updated_at = datetime.now()
        doc = self.to_json()
        doc.pop('id', None)
        return doc

    def prepare_update(self) -> dict:
        if not self.__loaded:
            raise ValueError("This class is not loaded, so it can not be updated.")
        self.updated_at = datetime.now()
        doc = self.to_json()
        new_doc = {k: v for k, v in doc.items() if k not in ['id', '_id'] and v is not None}
        return new_doc

    def insert(self) -> str:
        doc = self.prepare_insert()
        self._id = str(self.col.insert_one(doc).inserted_id)
        self.__loaded = True
        return self._id

    def update(self):
        if self.check_id_supplied():
            self.before_update()
            doc = self.prepare_update()
            return self.col.update_one({'_id': ObjectId(self._id)}, {'$set': doc})

    def update_many(self, conditions: dict, doc: dict):
        doc['updated_at'] = datetime.now()
        doc.pop('_id', None)
        return self.col.update_many(conditions, {'$set': doc})

    def update_one(self, conditions: dict, doc: dict):
        from pymongo.collection import ReturnDocument
        doc['updated_at'] = datetime.now()
        doc.pop('_id', None)
        return self.col.find_one_and_update(conditions, {'$set': doc}, return_document=ReturnDocument.AFTER)

    def delete(self):
        if self.check_id_supplied():
            return self.col.delete_one({'_id': ObjectId(self._id)}).raw_result

    def delete_one(self, conditions):
        return self.col.delete_one(conditions)

    def load(self) -> bool:
        result = None
        if not self.check_id_supplied():
            raise TypeError("id has not been initialized.")
        if self.col is None:
            raise TypeError("self.col has not been initialized.")
        try:
            result = self.col.find_one({"_id": ObjectId(self._id)})
        except Exception as e:
            logger_exceptions.error(str(e))
        if result is None:
            result = {}
        else:
            result['_id'] = str(result['_id'])
            self.load_result(result)
        self.__loaded = bool(result)
        return self.__loaded

    def is_loaded(self):
        return self.__loaded

    def exists(self, key, value) -> str:
        return self.col.find_one({key: value}) is not None

    def list(self, query=None) -> List:
        if query is None:
            query = {}
        result = self.col.find(query)
        instances = []
        for item in result:
            instance = self.__class__(db=self.db)
            for key, value in item.items():
                if hasattr(instance, key):
                    setattr(instance, key, str(value) if key == '_id' else value)
            instances.append(instance)
        return instances

    def list_json(self, query=None) -> List:
        if query is None:
            query = {}
        result = self.col.find(query)
        return self.serialize_list(result)

    def count(self, query=None) -> int:
        if query is None:
            query = {}
        return self.col.count_documents(query)

    def set_payload(self, payload):
        if payload is None:
            raise ValueError(f"Payload is None for {self.module_name}")
        try:
            for key, value in payload.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid attribute '{key}' for {self.module_name}")
            self.__loaded = True
        except ValueError:
            raise ValueError("An error with the values of payload happened")
        except AttributeError:
            raise ValueError("An error with the attributes of payload happened")
