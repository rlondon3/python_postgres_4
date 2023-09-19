from models.user import User_Store

store = User_Store()

class User_Handler():
    def create_account(self):
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
                return user
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
    