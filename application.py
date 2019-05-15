import socket
import spacy
import base64
from urllib.request import urlopen


pretrainedmodel = spacy.load("en_core_web_sm")


from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route("/nertext")
def nertext():
    return "hello world"
