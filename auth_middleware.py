#auth_middleware.py
from functools import wraps
import jwt
from flask import request, jsonify, make_response
from flask import current_app
import models.user as users

def token_required(user_type):
    def token_required_inner(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                try:
                    token_parts = request.headers["Authorization"].split(" ")
                    # Ensure the Authorization header is formatted as "Bearer <token>"
                    if len(token_parts) == 2 and token_parts[0] == "Bearer":
                        token = token_parts[-1]
                except Exception as e:
                    return make_response(jsonify({"message": "Token is missing or invalid", "error": str(e)}), 401)
            if not token:
                return make_response(jsonify({"message": "Authentication Token is missing!", "error": "Unauthorized"}), 401)

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                # Assuming the user type is part of the token's data
                if data.get("user_type") != user_type:
                    return make_response(jsonify({"message": "Invalid user type!", "error": "Unauthorized"}), 401)

                current_user = users.User().get_user_by_registro(data["registro"], user_type)
                if current_user is None:
                    return make_response(jsonify({"message": "Invalid Authentication token!", "error": "Unauthorized"}), 401)

            except Exception as e:
                return make_response(jsonify({"message": "Something went wrong", "error": str(e)}), 500)

            return f(current_user, *args, **kwargs)

        return decorated
    return token_required_inner
