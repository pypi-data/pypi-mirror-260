from flask import Flask, request
from base64 import b64decode
from random import randint
import os
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/upload", methods=["POST"])
def handle_response():
    json_data = request.get_json(silent=False)
    _id = str(randint(1, 99999)) + str(randint(1, 99999))
    os.mkdir("uploaded_files/" + _id)
    with open("uploaded_files/" + _id + "/snapshot.pickle", "wb")as f:
        f.write(b64decode(json_data["snapshot"].encode()))
    with open("uploaded_files/" + _id + "/log.txt", "wb") as f:
        f.write(b64decode(json_data["log"].encode()))
    return "<p>success</p>"
