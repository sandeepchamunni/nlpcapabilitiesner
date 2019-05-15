from flask import Flask
import spacy
import base64
from urllib.request import urlopen
#from urllib.request import urlopen

pretrainedmodel = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route("/")
def hello():
    documentContents = request.args.get('contents')
    doc2 = pretrainedmodel(documentContents)
    JSONOut = "{\"contents\" : \"" + str(base64.b64encode(bytes(documentContents,"utf-8"))).replace("b'","") + "\", \"ner\" : ["
    for ent in doc2.ents:
       JSONOut += "{\"label\" : \"" + ent.label_ + "\", \"text\" : \"" + str(base64.b64encode(bytes(ent.text,"utf-8"))).replace("b'","") + "\",\"start\" : \"" + str(ent.start_char) + "\",\"end\" : \"" + str(ent.end_char) + "\"},"
    return JSONOut
