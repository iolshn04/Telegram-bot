import peewee as pw
from datetime import datetime


db = pw.SqliteDatabase('history.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class User(ModelBase):
    external_id = pw.BigIntegerField(unique=True)
    chat_id = pw.BigIntegerField(unique=True)


class History(ModelBase):
    user = pw.ForeignKeyField(User)
    created_command = pw.DateField(default=datetime.now())
    message = pw.TextField()
