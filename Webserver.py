from flask import Flask, request
import pickle
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def result():
    handleInput(request.data)
    return "Request gotten"

def handleInput(commandJSON):
    
    print(json.loads(commandJSON))