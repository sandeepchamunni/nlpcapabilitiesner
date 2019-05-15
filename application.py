from flask import Flask
import spacy
import base64
#from urllib.request import urlopen
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
