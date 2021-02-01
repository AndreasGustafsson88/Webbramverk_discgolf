from App.Data.DB_SETTINGS import LOCALHOST, USER, PASSWORD, DB_NAME
from pymongo import MongoClient
from abc import ABC

# client = MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@cluster0.f9uyc.mongodb.net/{DB_NAME}?retryWrites=true&w=majority')
client = MongoClient(f'mongodb://root:password@localhost:27027')
db = client.discgolf


class ResultList(list):

    def first_or_none(self):
        return self[0] if len(self) > 0 else None

    def last_or_none(self):
        return self[-1] if len(self) > 0 else None


class Document(dict, ABC):
    collection = None

    def __init__(self, data):
        super().__init__()
        if '_id' not in data:
            self._id = None
        self.__dict__.update(data)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return '\n'.join(f'{k} = {v}' for k, v in self.__dict__.items())

    def save(self):
        if not self._id:
            del(self.__dict__['_id'])
            return self.collection.insert_one(self.__dict__)
        else:
            return self.collection.update({'_id': self._id}, self.__dict__)

    def delete_field(self, field):
        return self.collection.update({'_id': self._id}, {"$unset": {field: ""}})

    def update_field(self, field, value):
        return self.collection.update_one({'_id': self._id}, {"$set": {field: value}})

    def update_user_settings(self, profile_picture, user_name, email, password):
        return self.collection.update.one({'_id': self._id}, {'$set': {
            'profile_picture': profile_picture,
            'user_name': user_name,
            'email': email,
            'password': password
        }})

    @classmethod
    def insert_many(cls, items):
        cl_objects = []
        for item in items:
            cl_objects.append(cls.insert_one(item))

        return cl_objects

    @classmethod
    def insert_one(cls, item):
        cl_object = cls(item)
        cl_object.save()
        return cl_object

    @classmethod
    def all(cls):
        return [cls(item) for item in cls.collection.find({})]

    @classmethod
    def find_unique(cls, **kwargs):
        return cls(cls.collection.find_one(kwargs)) if cls.collection.find_one(kwargs) else None

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

    @classmethod
    def delete_many(cls, **kwargs):
        return cls.collection.delete_many(kwargs)

    @classmethod
    def delete_one(cls, **kwargs):
        return cls.collection.delete_one(kwargs)






