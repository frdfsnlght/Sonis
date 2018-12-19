
from peewee import *

from ..db import db, SonisModel, addModel


class Version(SonisModel):
    name = CharField(unique = True)
    version = IntegerField()
    
    class Meta:
        database = db
        only_save_dirty = True

addModel(Version)
