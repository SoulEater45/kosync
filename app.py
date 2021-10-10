from flask import Flask
from kosync import kosync

app = Flask(__name__)
app.register_blueprint(kosync)
