from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import os
import re

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


GET_USER = "SELECT * FROM users WHERE id = %s;"
GET_USERS = "SELECT * FROM users;"
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY, 
                        first_name VARCHAR (100) NOT NULL, 
                        last_name VARCHAR (100) NOT NULL,
                        birthday DATE,
                        city VARCHAR (100) NOT NULL,
                        state VARCHAR (2) NOT NULL, 
                        active BOOLEAN NOT NULL,
                        user_name VARCHAR (50) NOT NULL,
                        email VARCHAR (50) NOT NULL,
                        password VARCHAR (255) NOT NULL
                        )"""
INSERT_INTO_USERS_TABLE_RETURNING_ID = """INSERT INTO users (
                                        first_name, 
                                        last_name,
                                        birthday, 
                                        city, 
                                        state, 
                                        active,
                                        user_name, 
                                        email, 
                                        password
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
UPDATE_USERS_TABLE_RETURNING_USER = """UPDATE users SET 
                                    first_name=(%s), 
                                    last_name=(%s), 
                                    birthday=(%s), city=(%s), 
                                    state=(%s), 
                                    active=(%s),
                                    user_name=(%s), 
                                    email=(%s), 
                                    password=(%s) WHERE id=(%s) RETURNING *;"""
DELETE_FROM_USERS_RETURNING_ID = "SELECT FROM users WHERE id = (%s);"

class User_Store:
    def index(self):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_USERS)
                connection.commit()
                user = cursor.fetchall()
                if user:
                    return user
                else:
                    return {"error": "Users not found"}
                
    def show(self, id):
        data = request.get_json()
        id = data["id"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_USER, (id,))
                connection.commit()
                user = cursor.fetchone()
                try:
                    if user:
                        return user
                except Exception as e:
                    cursor.close()
                    return {"error": str(e)}
            
    def create(self):
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        birthday = data['birthday']
        city = data['city']
        state = data['state']
        active = data['active']
        user_name = data['user_name']
        email = data['email']
        password = data['password']

        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(CREATE_USERS_TABLE)
                cursor.execute(GET_USER, (user_name,)) # Need to change this to id in the SQL
                user = cursor.fetchone()
                if user:
                    return {"message": "User already exists. Please login."}
                elif not re.match(r'[\w.]+\@[\w.]+', email):
                    print(user_name, email, 'email')
                    return {"message": "Invalid: please check email address."}
                elif not re.match(r'[A-Za-z0-9]+', user_name):
                    return {"message": "Invalid: username must contain only characters and numbers."}
                elif not user_name or not password or not email:
                    return {"message": "Invalid: please check username, email, and password."}
                else:
                    cursor.execute(INSERT_INTO_USERS_TABLE_RETURNING_ID, (first_name, last_name, birthday, city, state, active, user_name, email, generate_password_hash(password)))
                    connection.commit()
                    return {"message": "User successful registered"}, 201
                
    def update(self):
        try:
            data = request.get_json()
            id = data['id']
            first_name = data['first_name']
            last_name = data['last_name']
            birthday = data['birthday']
            city = data['city']
            state = data['state']
            active = data['active']
            user_name = data['user_name']
            email = data['email']
            password = data['password']
            with connection:
                with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute(GET_USER, (id,))
                    user = cursor.fetchone()
                    if user:
                        cursor.execute(UPDATE_USERS_TABLE_RETURNING_USER, (first_name, last_name, birthday, city, state, active, user_name, email, generate_password_hash(password), id))
                        connection.commit()
        except Exception as e:
            return {
                "error": str(e)
            }

    def delete(self, id):
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_FROM_USERS_RETURNING_ID, (id,))
                    connection.commit()
                    return cursor.fetchone()[0]

        except Exception as e:
            return {
                "error": str(e)
            }
