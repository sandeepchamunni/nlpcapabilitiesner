from flask import Flask,redirect, url_for, request
import spacy
import base64
from urllib.request import urlopen
#from urllib.request import urlopen

pretrainedmodel = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route("/nerfile")
def nerfile():
    docpath = request.args.get('document')
    modelpath = request.args.get('modelpath')
    nlp2 = spacy.load(modelpath) 
    inputDocument = urlopen(docpath)
    documentContents = inputDocument.read().decode("utf-8")
    doc2 = nlp2(documentContents)
    JSONOut = "{\"contents\" : \"" + str(base64.b64encode(bytes(documentContents,"utf-8"))).replace("b'","") + "\", \"ner\" : [" 
    for ent in doc2.ents:
       JSONOut += "{\"label\" : \"" + ent.label_ + "\", \"text\" : \"" + str(base64.b64encode(bytes(ent.text,"utf-8"))).replace("b'","") + "\",\"start\" : \"" + str(ent.start_char) + "\",\"end\" : \"" + str(ent.end_char) + "\"},"
    return JSONOut

@app.route("/nerpretrainedfile")
def nerpretrainedfile():
    docpath = request.args.get('document')
    inputDocument = urlopen(docpath)
    documentContents = inputDocument.read().decode("utf-8")
    doc2 = pretrainedmodel(documentContents)
    JSONOut = "{\"contents\" : \"" + str(base64.b64encode(bytes(documentContents,"utf-8"))).replace("b'","") + "\", \"ner\" : ["
    for ent in doc2.ents:
       JSONOut += "{\"label\" : \"" + ent.label_ + "\", \"text\" : \"" + str(base64.b64encode(bytes(ent.text,"utf-8"))).replace("b'","") + "\",\"start\" : \"" + str(ent.start_char) + "\",\"end\" : \"" + str(ent.end_char) + "\"},"
    return JSONOut  

@app.route("/nertext")
def nertext():
    modelpath = request.args.get('modelpath')
    documentContents = request.args.get('contents')
    nlp2 = spacy.load(modelpath)
    doc2 = nlp2(documentContents)
    JSONOut = "{\"contents\" : \"" + str(base64.b64encode(bytes(documentContents,"utf-8"))).replace("b'","") + "\", \"ner\" : ["
    for ent in doc2.ents:
       JSONOut += "{\"label\" : \"" + ent.label_ + "\", \"text\" : \"" + str(base64.b64encode(bytes(ent.text,"utf-8"))).replace("b'","") + "\",\"start\" : \"" + str(ent.start_char) + "\",\"end\" : \"" + str(ent.end_char) + "\"},"
    return JSONOut
  
@app.route("/nerpretrainedtext")
def nerpretrainedtext():
    documentContents = request.args.get('contents')
    doc2 = pretrainedmodel(documentContents)
    JSONOut = "{\"contents\" : \"" + str(base64.b64encode(bytes(documentContents,"utf-8"))).replace("b'","") + "\", \"ner\" : ["
    for ent in doc2.ents:
       JSONOut += "{\"label\" : \"" + ent.label_ + "\", \"text\" : \"" + str(base64.b64encode(bytes(ent.text,"utf-8"))).replace("b'","") + "\",\"start\" : \"" + str(ent.start_char) + "\",\"end\" : \"" + str(ent.end_char) + "\"},"
    return JSONOut
