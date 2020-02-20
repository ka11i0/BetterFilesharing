import requests
from flask import Flask, render_template, redirect, request, url_for, session
from flaskapp import app

@app.route("/view_shell", methods=['GET', 'POST'])
def view_shell():
    return "bobo"

@app.route("/send_shell", methods=['GET', 'POST'])
def send_shell():
    return "suger"

@app.route("/receive_shell", methods=['GET', 'POST'])
def receive_shell():
    return "hihi :)"