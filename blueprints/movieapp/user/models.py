from flask import jsonify, session, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from ....extensions import mongo

class User:
    def signup(self, form):
        """Handles user registration with proper validation and JWT authentication."""
        
        # Create a new user object
        user = {
            "username": form.username.data,
            "email": form.email.data,
            "password": pbkdf2_sha256.hash(form.password.data),  # Hash the password
        }

        # Check for duplicate email
        if mongo.db.users.find_one({"email": user["email"]}):
            return jsonify({"error": "Email already registered"}), 400

        try:
            result = mongo.db.users.insert_one(user)

            if result.inserted_id:
                user["_id"] = str(result.inserted_id)
                return self.start_session(user)
            else:
                return jsonify({"error": "Signup failed"}), 400

        except Exception as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    def login(self, form):
        """Handles user authentication and JWT generation."""
        
        user = mongo.db.users.find_one({"email": form.email.data})

        if user and pbkdf2_sha256.verify(form.password.data, user["password"]):
            user["_id"] = str(user["_id"])
            return self.start_session(user)
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    def start_session(self, user):
        """Creates a session with JWT stored in HTTP-only cookies."""

        # Generate JWT access and refresh tokens
        access_token = create_access_token(identity=user["_id"], expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user["_id"])

        csrf_token = get_csrf_token(access_token)

        # Remove sensitive data before storing in session
        del user["password"]
        session["logged_in"] = True
        session["user"] = user

        # Set JWT in HTTP-only cookies
        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("csrf_access_token", csrf_token, httponly=False, secure=True, samesite="Strict")

        return response

    def logout(self):
        """Logs out user by clearing the session and JWT cookies."""
        
        session.clear()
        response = make_response(jsonify({"message": "Logged out successfully"}), 200)
        response.set_cookie("access_token", "", expires=0, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("refresh_token", "", expires=0, httponly=True, secure=True, samesite="Strict")

        return response
