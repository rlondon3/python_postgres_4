from dotenv import load_dotenv
from flask import request, Flask
from functools import wraps
from datetime import datetime, timedelta
from config import secret_key
import jwt
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def generate_auth_token(user_id):
    try:
        payload ={
            'eexpiration': str(datetime.utcnow() + timedelta(seconds=60)),
            'iat': str(datetime.utcnow()),
            'user_id': user_id
        }
        return jwt.encode(
            payload, 
            app.config['SECRET_KEY'],
        )
    except Exception as e:
        return {'error': str(e)}
    
def verify_auth_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'])
        if payload['user_id']:
            return payload['user_id']
    except jwt.ExpiredSignatureError:
        return {'error': 'Signature expired. Please login again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token. Please login again.'}
def authToken():
    headers = request.headers
    # auth = headers.get("some name")
    

