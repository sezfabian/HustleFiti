from flask import Flask, render_template, request
from flask_cors import CORS
import os

from models import storage

print(storage.all())