from flask import Flask, render_template, request, redirect
from flaskapp import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contracts')
def contracts():
    return render_template('contracts.html')

@app.route('/files')
def files():
    return render_template('files.html')