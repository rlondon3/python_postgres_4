from dotenv import load_dotenv
from flask import request, Flask
from datetime import datetime, timedelta
from models.user import User_Store
import jwt
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def generate_auth_token(user_id):
    try:
        payload = { 
            'expiration': str(datetime.utcnow() + timedelta(seconds=60)),
            'iat': datetime.utcnow(),
            'user_id': user_id
        }
        return jwt.encode(
            payload, 
            app.config['SECRET_KEY'],
            algorithm="HS512",
        )
    except Exception as e:
        return {'error': str(e)}
    
# Verify the auth token set in the header by decoding the auth token    
def verify_auth_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS512")
        if payload['user_id']:
            return payload['user_id']
        if jwt.ExpiredSignatureError:
            return {'error': 'Signature expired. Please login again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token. Please login again.'}
    
# Verify the user is authenticated by verifying the id from the decoded token
def authenticate_user_id():
    headers = request.headers
    try:
        auth_head = headers['Authorization']
        token = str(auth_head).split(' ')[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS512")
        for item in User_Store.User:
            if item == payload['user_id']:
                return {'auth_user': payload['user_id']}
    except jwt.InvalidTokenError:
        return {'error': "Invalid ID. "}
        
def authToken():
    headers = request.headers
    # auth = headers.get("some name")
    

