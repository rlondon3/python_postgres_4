from flask import Flask, request, session, make_response, jsonify
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


GET_USERS = "SELECT * FROM users;"

User = {
    "username": str,
    "password": str
}

class User_Store:
    def index(self):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_USERS)
                connection.commit()
                users = cursor.fetchall()
                try:
                    if users:
                      return {"Success": users}, 201  
                except:
                    cursor.close()
                    return {"Failed": "No users found"}
