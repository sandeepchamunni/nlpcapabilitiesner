# -*- coding: utf-8 -*-
import spacy
import base64
from urllib.request import urlopen

#spacy.cli.download("en")

#pretrainedmodel = spacy.load("en_core_web_sm")


from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route("/nerfile")
def nerfile():
    return "Hello world"
