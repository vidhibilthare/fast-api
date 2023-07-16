from tortoise.models import Model
from tortoise import Tortoise,fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200)
    email = fields.CharField(200,unique = True)
    mobile = fields.CharField(10)
    password = fields.CharField(250)

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200)
    email = fields.CharField(200,unique = True)
    mobile = fields.CharField(10)
    password = fields.CharField(250)


Tortoise.init_models(['user.models'],'models')