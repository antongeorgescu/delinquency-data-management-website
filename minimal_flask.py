#!/usr/bin/env python3
import sys
print("Python executable:", sys.executable)

from flask import Flask
print("Flask imported successfully")

from flask_cors import CORS
print("Flask-CORS imported successfully")

app = Flask(__name__)
CORS(app)
print("CORS enabled")

@app.route('/')
def hello():
    return "Hello World"

print("Starting Flask app...")
app.run(debug=True, port=5001)