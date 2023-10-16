from flask import Flask, render_template, request
from flask_cors import CORS
import os
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.mail import Email
storage = DBStorage()
mail = Email()
storage.reload()

print(storage.all())
