from flask import Flask
from kosync import kosync

app = Flask(__name__)
app.register_blueprint(kosync)

if __name__ == '__main__':
    app.run(host='0.0.0.0')