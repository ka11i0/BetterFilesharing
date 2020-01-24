from flask import Flask, render_template, request, redirect
from flaskapp import app


@app.route('/')
def index():
    return render_template('index.html')

