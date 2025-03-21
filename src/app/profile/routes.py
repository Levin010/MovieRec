from flask import Blueprint, render_template, session, redirect, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from werkzeug.utils import secure_filename
from ..profile.forms import UpdateProfileForm
from ....extensions import mongo
import os

profile_bp = Blueprint('profile', __name__) 

UPLOAD_FOLDER = 'static/uploads/profilepic/' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@profile_bp.route('/userprofile/')
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})

    if not user:
        return redirect("/user/login")

    return render_template('profile/userprofile.html', user=user)

@profile_bp.route('/update/', methods=['PATCH'])
@jwt_required()
def update_profile():
    
    user_id = get_jwt_identity()
    form = UpdateProfileForm(formdata=request.form)
    form.profile_picture.data = request.files.get('profile_picture')

    if form.validate():
        update_data = {}

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                
                if file_ext not in ALLOWED_EXTENSIONS:
                    return jsonify({"error": "Only PNG, JPG, and JPEG files are allowed"}), 400

                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                relative_path = f"uploads/profilepic/{filename}"
                update_data["profile_picture"] = relative_path
                print(f"Full filepath saved to disk: {filepath}")
                print(f"Relative path saved to database: {relative_path}")

        for key in ["given_name", "family_name", "location", "bio", "pronoun"]:
            value = request.form.get(key)
            if value:
                update_data[key] = value

        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return jsonify({"message": "Profile updated successfully"}), 200

    return jsonify({"error": "Invalid input"}), 400

@profile_bp.route('/get_profile/', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user['_id'] = str(user['_id'])
    
    if 'password' in user:
        del user['password']
    
    return jsonify(user), 200


@profile_bp.route('/userprofileee/')
@jwt_required()
def user_profileee():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})

    if not user:
        return redirect("/user/login")

    return render_template('profile/userprofileee.html', user=user)