import hashlib

from flask import Blueprint

kosync = Blueprint("kosync", __name__, url_prefix="/kosync")

@kosync.route("/")
def index():
    return("This is an example")
