from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import Optional, Length
from flask_wtf.file import FileAllowed, FileRequired

class UpdateProfileForm(FlaskForm):
    given_name = StringField("Given Name", validators=[Optional(), Length(max=50)])
    family_name = StringField("Family Name", validators=[Optional(), Length(max=50)])
    profile_picture = FileField("Profile Picture", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], "Only JPG and PNG allowed")])
    location = StringField("Location", validators=[Optional(), Length(max=100)])
    bio = StringField("Bio", validators=[Optional(), Length(max=500)])
    pronoun = StringField("Pronoun", validators=[Optional(), Length(max=30)])
    
    class Meta:
        csrf = False
