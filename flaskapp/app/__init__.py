#!/usr/bin/python3
from flask import Flask

def create_app():
    """flask app initializer"""
    app = Flask(__name__)
    return app

