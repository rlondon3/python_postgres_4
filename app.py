from flask import Flask, request, session, make_response, jsonify
from dotenv import load_dotenv
from models.user import User_Store
import psycopg2
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

store = User_Store()

@app.post("/admin/users") # Need to add auth to visit this route
def get_users():
    users = store.index()
    try:
        if users: # Need error handling
            return users    
    except:
        return {"message": "failed"}, 404
    
@app.post("/user/signup")
def create_account():
    user = store.create()
    try:
        if user:
            return user
    except Exception as e:
        return {"error" : str(e)}