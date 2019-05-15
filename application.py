from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route("/nertext")
def nertext():
    return "hello world"
