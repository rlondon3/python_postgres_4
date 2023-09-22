from flask import request
from dotenv import load_dotenv
from database import connection
from migrations.sql.users.user_statements import ( GET_USER_BY_USERNAME, GET_USER_BY_ID, GET_USERS, 
                                                  CREATE_USERS_TABLE, INSERT_INTO_USERS_TABLE_RETURNING_ID, 
                                                  UPDATE_USERS_TABLE_RETURNING_USER, DELETE_FROM_USERS_RETURNING_ID 
                                                  )
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras
import re

load_dotenv()

#Instantiate a class that holds user schema as methods
class User_Store:
    # Get all users
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
    # Get user by id            
    def show(self, id):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_USER_BY_ID, (id,))
                connection.commit()
                user = cursor.fetchone()[0]
                try:
                    if user:
                        return user
                except Exception as e:
                    cursor.close()
                    return {"error": str(e)}
    # Create a user        
    def create(self, first_name, last_name, birthday, city, state, zip, active, user_name, email, password):
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(CREATE_USERS_TABLE)
                cursor.execute(GET_USER_BY_USERNAME, (user_name,)) # Need to change this to id in the SQL
                user = cursor.fetchone()
                if user:
                    return {"message": "User already exists. Please login."}
                elif not re.match(r'[\w.]+\@[\w.]+', email):
                    return {"message": "Invalid: please check email address."}
                elif not re.match(r'[A-Za-z0-9]+', user_name):
                    return {"message": "Invalid: username must contain only characters and numbers."}
                elif not user_name or not password or not email:
                    return {"message": "Invalid: please check username, email, and password."}
                else:
                    cursor.execute(INSERT_INTO_USERS_TABLE_RETURNING_ID, (first_name, last_name, birthday, 
                                                                          city, state, zip, active, user_name, email, 
                                                                          generate_password_hash(password))
                                                                          )
                    connection.commit()
                    return {"message": "User successful registered"}, 201
    # Update a user            
    def update(self, user_id, first_name, last_name, birthday, city, state, zip, active, user_name, email, password):
        if user_id:
            try:
                with connection:
                    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                        cursor.execute(GET_USER_BY_ID, (user_id,))
                        user = cursor.fetchone()[0]
                        if user:
                            cursor.execute(UPDATE_USERS_TABLE_RETURNING_USER, (first_name, last_name, birthday, 
                                                                            city, state, zip, active, user_name, email, 
                                                                            generate_password_hash(password), user_id)
                                                                            )
                            connection.commit()
                            return user
            except Exception as e:
                return {
                    {"error": str(e)}
                }
    # Delete a user
    def delete(self, user_id):
        if user_id:
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(DELETE_FROM_USERS_RETURNING_ID, (user_id,))
                        connection.commit()
                        user = cursor.fetchone()[0]
                        return {"user_id": user}

            except Exception as e:
                return {
                    {"error": str(e)}
                }
    def authenticate(self, username, password):
        try:
            with connection:
                with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute(GET_USER_BY_USERNAME, (username,))
                    user = cursor.fetchone()
                    if user:
                        hashed_password = user['password']
                        if check_password_hash(hashed_password, password):
                            return {"user": user}
                    else:
                        return {"message": "Account not found!"}
        except Exception as e:
            return {
                    {"error": str(e)}
                }