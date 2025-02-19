from flask import Flask, jsonify, request, session, redirect
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from extensions import db

class User:
    def signup(self):

        # create a new user object
        user = {
            #"id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
        } 

        # hash the password
        user['password'] = pbkdf2_sha256.hash(user['password'])


        # prevent duplicate email
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use. Try again."}), 400


        try:
            result = db.users.insert_one(user)
    
            # If insertion was successful, result.inserted_id will exist
            if result.inserted_id:
                user['_id'] = str(result.inserted_id)
                return self.start_session(user)
            else:
                return jsonify({"error": "Signup failed"}), 400

        except Exception as e:
            # Handle any database errors
            return jsonify({"error": "Signup failed", "message": str(e)}), 400
        
        #result = db.users.insert_one(user)

        #user['_id'] = str(result.inserted_id)


        #return jsonify(user), 200
    
    def start_session(self, user):
        user['_id'] = str(user['_id'])
        del user['password']
        session['logged_in'] = True
        session['user'] = user  
        return jsonify(user), 200
    
    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        else:
            return jsonify({"error": "Invalid login credentials"}), 401