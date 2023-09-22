from flask import Flask
from handlers.user_handler import user_route  
from database import connect


app = Flask(__name__)
app.config['SECRET_KEY']

@app.get("/")
def connect_db():
    return connect()

user_routes = user_route(app)  

