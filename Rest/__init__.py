#!/usr/bin/python
from flask import Flask, url_for

BASE_URL = "/v1"
app = Flask(__name__)

from Rest.contract import put_contract
