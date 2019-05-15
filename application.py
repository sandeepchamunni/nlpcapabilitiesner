# -*- coding: utf-8 -*-
from flask import Flask, request
from azure.storage.blob import BlockBlobService
import docx
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import os,os.path
import json

def getTextfromdoc(filename):
            
            #print(fileExtension)
            doc = docx.Document(filename)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)

def pdfparser(data):

            fp = open(data, 'rb')
            rsrcmgr = PDFResourceManager()
            retstr = io.StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            # Create a PDF interpreter object.
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # Process each page contained in the document.

            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
                data =  retstr.getvalue()
            return data         

app = Flask(__name__)
@app.route("/upload")
def upload():
    try:
                    
        download_folder = './nlp_inputs'
        for root, dirs, files in os.walk(download_folder):
            for file in files:
                os.remove(os.path.join(root, file))
                
        os.makedirs(download_folder, exist_ok=True)
        fileName_ext = request.args.get('filename')
        containerName = request.args.get('containername')

        fileExtension=fileName_ext.split(".")[-1] 
        fileName=os.path.splitext(fileName_ext)[0]
        
        block_blob_service = BlockBlobService(account_name='nlpcapabilities', account_key='Zwg41Q5jHTTzBIylmn7g/x4nn99iGEVzeDR/ib6x2fSEEjvHFhsYuUxgWBfapIPJ/gQHmb+WzmLPUf/0hX7ZwQ==')
        block_blob_service.get_blob_to_path(containerName, fileName_ext,download_folder+'/'+fileName_ext)
        
        if fileExtension=="docx":
            data=getTextfromdoc(download_folder+'/'+fileName_ext)
            with open(download_folder+'/'+fileName+".txt", "w",encoding="utf-8") as text_file:
                text_file.write(data)
        elif fileExtension=="pdf":
            data=pdfparser(download_folder+'/'+fileName_ext)
            with open(download_folder+'/'+fileName+".txt", "w",encoding="utf-8") as text_file:
                text_file.write(str(data))
        elif fileExtension=="txt":
            pass
            
        else:
            result={
                    "Status": "Failure",
                    "Error Message": "Incorrect file format."
                }
            return json.dumps(result)
        result={
                    "Status": "Success"
                }
        return json.dumps(result)
                       
    except Exception as e:
        er_details=str(e)
        print ("Execution terminated")
        result={
                "Status": "Failure",
                "Error Message": er_details
            }
        return json.dumps(result)
