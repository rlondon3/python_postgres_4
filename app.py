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

app.add_url_rule("/users/signup", "create_user", handler.create_account, methods=["POST"])
app.add_url_rule("/admin/users", "show_users", handler.get_users, methods=["POST"]) #ADD AUTH
app.add_url_rule("/admin/user/<int:id>", "show_user", handler.get_user, methods=["POST"])
app.add_url_rule("/users/<int:id>", "update_user", handler.update_user, methods=["PUT"])
app.add_url_rule("/users/<int:id>", "delete_user", handler.delete_user, methods=["DELETE"])
    