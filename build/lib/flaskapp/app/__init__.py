#!/usr/bin/python3
from flask import Flask
from .extensions import api, db
from .services_resources import ns
import os

def create_app():
    """flask app initializer"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") 
    api.init_app(app)
    db.init_app(app)
    api.add_namespace(ns)
    return app

