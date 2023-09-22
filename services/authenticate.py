from dotenv import load_dotenv
from flask import Flask, request, jsonify
from functools import wraps
from models.user import User, User_Store
import jwt
import os

load_dotenv()
app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert': 'Token missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"Alert": "Invalid Token"})
    return decorated

def authToken():
    headers = request.headers
    

