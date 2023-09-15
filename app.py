from flask import Flask
from models.user import User_Store
from database import connect


app = Flask(__name__)

store = User_Store()

@app.route("/")
def connect_db():
    return connect()

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