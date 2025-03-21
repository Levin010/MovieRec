from flask import jsonify, session, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from ....extensions import mongo

class User:
    def signup(self, form):
        
        user = {
            "username": form.username.data,
            "email": form.email.data,
            "password": pbkdf2_sha256.hash(form.password.data),
            "given_name": None,
            "family_name": None,
            "profile_picture": None,
            "location": None,
            "bio": None,
            "pronoun": None
        }

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
        
        user = mongo.db.users.find_one({"email": form.email.data})

        if user and pbkdf2_sha256.verify(form.password.data, user["password"]):
            user["_id"] = str(user["_id"])
            return self.start_session(user)
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    def start_session(self, user):
        """Creates a session with JWT stored in HTTP-only cookies."""

        access_token = create_access_token(identity=user["_id"], expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user["_id"])

        csrf_token = get_csrf_token(access_token)

        del user["password"]
        session["logged_in"] = True
        session["user"] = user

        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("csrf_access_token", csrf_token, httponly=False, secure=True, samesite="Strict")

        return response

    def logout(self):
        
        session.clear()
        response = make_response(jsonify({"message": "Logged out successfully"}), 200)
        response.set_cookie("access_token", "", expires=0, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("refresh_token", "", expires=0, httponly=True, secure=True, samesite="Strict")

        return response
