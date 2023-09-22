from models.user import User_Store

store = User_Store()

class User_Handler():
    def create_account():
        try:
            user = store.create()
            if user:
                return user
        except Exception as e:
            return {"error" : str(e)}

    def get_users():
        try:
            users = store.index()
            if users: # Need error handling
                return users    
        except Exception as e:
            return {"error": str(e)}, 404
        
    def get_user(id):
        user_id = id
        try:
            user = store.show(user_id)
            if user:
                return user
        except Exception as e:
            return {"error": str(e)}

    def update_user(id):
        user_id = id
        try:
            user = store.update(user_id)
            if user:
                return {"updated user": user}
        except Exception as e:
            return {"error": str(e)}

    def delete_user(id):
        user_id = id
        try:
            user = store.delete(user_id)
            if user:
                return user
        except Exception as e:
            return {"error": str(e)}


def user_route(app):
    app.add_url_rule("/users/signup", "create_user", User_Handler.create_account, methods=["POST"])
    app.add_url_rule("/admin/users", "show_users", User_Handler.get_users, methods=["POST"]) #ADD AUTH
    app.add_url_rule("/admin/user/<int:id>", "show_user", User_Handler.get_user, methods=["POST"])
    app.add_url_rule("/users/<int:id>", "update_user", User_Handler.update_user, methods=["PUT"])
    app.add_url_rule("/users/<int:id>", "delete_user", User_Handler.delete_user, methods=["DELETE"])