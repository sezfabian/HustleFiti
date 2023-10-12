#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.mail import Email


storage = DBStorage()
mail = Email()
storage.reload()
