from models.user import User_Store
from flask import request, make_response, jsonify
from services.authenticate import generate_auth_token, authenticate_user_id


store = User_Store()

class User_Handler():
    def create_account():
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        birthday = data['birthday']
        city = data['city']
        state = data['state']
        zip = data["zip"]
        active = data['active']
        user_name = data['user_name']
        email = data['email']
        password = data['password']
        try:
            user = store.create(first_name, last_name, birthday, city, state, zip, active, user_name, email, password)
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
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        birthday = data['birthday']
        city = data['city']
        state = data['state']
        zip = data['zip']
        active = data['active']
        user_name = data['user_name']
        email = data['email']
        password = data['password']
        try:
            user = store.update(user_id, first_name, last_name, birthday, city, state, zip, active, user_name, email, password)
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
        
    def authenticate():
        try:
            data = request.get_json()
            username = data['user_name']
            password = data['password']
            authenticated_user = store.authenticate(username, password)
            if authenticated_user is None:
                return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})
            else:
                token = generate_auth_token(authenticated_user['user'][0])
                return jsonify({"token": token}) 

        except Exception as e:
            return {"error": str(e)}
        
def user_route(app):
    app.add_url_rule("/users/signup", "create_user", User_Handler.create_account, methods=["POST"])
    app.add_url_rule("/admin/users", "show_users", User_Handler.get_users, methods=["POST"]) #ADD AUTH
    app.add_url_rule("/admin/user/<int:id>", "show_user", User_Handler.get_user, methods=["POST"])
    app.add_url_rule("/users/<int:id>", "update_user", User_Handler.update_user, methods=["PUT"])
    app.add_url_rule("/users/<int:id>", "delete_user", User_Handler.delete_user, methods=["DELETE"])
    app.add_url_rule("/authenticate/user", "authenticate", User_Handler.authenticate, methods=['POST'])