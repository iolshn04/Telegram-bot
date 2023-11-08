import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('history.db')


class ModelBase(pw.Model):
    class Meta:
        database = db


class User(ModelBase):
    name = pw.CharField()
    external_id = pw.BigIntegerField(unique=True)
    chat_id = pw.BigIntegerField(unique=True)


class History(ModelBase):
    user = pw.ForeignKeyField(User)
    command = pw.TextField(null=True)
    message = pw.TextField(null=True)


db.create_tables([User, History])
