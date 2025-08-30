from flask import Flask, jsonify
from flask_cors import CORS 
import os

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)  
CORS(app)

