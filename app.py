from flask import Flask
from models.user import User_Store
from handlers.user_handler import User_Handler  
from database import connect


app = Flask(__name__)

store = User_Store()
handler = User_Handler()

@app.route("/")
def connect_db():
    return connect()

app.add_url_rule("/users/signup", "create", handler.create_account, methods=["POST"])

@app.post("/admin/users") # Need to add auth to visit this route
def get_users():
    try:
        users = store.index()
        if users: # Need error handling
            return users    
    except Exception as e:
        return {"error": str(e)}, 404
    
@app.post("/admin/user/<int:id>")
def get_user(id):
    user_id = id
    try:
        user = store.show(user_id)
        if user:
            return user
    except Exception as e:
        return {"error": str(e)}

@app.put("/users/<int:id>")
def update_user(id):
    user_id = id
    try:
        user = store.update(user_id)
        if user:
            return user
    except Exception as e:
        return {"error": str(e)}

@app.delete("/users/<int:id>")
def delete_user(id):
    user_id = id
    try:
        user = store.delete(user_id)
        if user:
            return user
    except Exception as e:
        return {"error": str(e)}
    