from flask import Flask
import spacy
import base64
from urllib.request import urlopen
#from urllib.request import urlopen

pretrainedmodel = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
