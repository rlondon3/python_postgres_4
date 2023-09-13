from flask import Flask, request, session, make_response, jsonify
from dotenv import load_dotenv
from models.user import User, User_Store
import psycopg2
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

store = User_Store()

@app.route("/")
def index():
    users = store.index()
    try:
        if users:
            return users
    except:
        return {"message": "failed"}, 404