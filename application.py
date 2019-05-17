from flask import Flask,redirect, url_for, request
import spacy
import base64
from urllib.request import urlopen
import random
import base64

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

@app.route("/nercustomtrain")
def nercustomtrain():
    TRAIN_DATA = [
        (u"Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
        (u"Jasmine is a flower", {"entities": [(0, 7, "FLOWER")]}),
        (u"Google rebrands its business apps", {"entities": [(0, 6, "ORG")]})]
    try:
      nlp = spacy.blank('en')
      ner = nlp.create_pipe("ner")
      nlp.add_pipe(ner, last=True)
      nlp.entity.add_label('FLOWER')
      nlp.entity.add_label('ORG')

      nlp.vocab.vectors.name = 'spacy_pretrained_vectors'
      optimizer = nlp.begin_training()
      for i in range(20):
          random.shuffle(TRAIN_DATA)
          for text, annotations in TRAIN_DATA:
              nlp.update([text], [annotations], sgd=optimizer)
      nlp.to_disk("/nlpcustommodel")
      return("Completed")
    except e as error:
      return str(e)
