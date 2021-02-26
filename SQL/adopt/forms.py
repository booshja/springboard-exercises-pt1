from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange


class AddPetForm(FlaskForm):
    """Form for adding a pet"""

    pet_name = StringField('Pet Name', validators=[
                           InputRequired(message='Pet name cannot be left blank')])
    species = SelectField('Category', choices=[
                          ('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    url = StringField('Photo URL', validators=[Optional(), URL(
        require_tld=True, message="Must be a valid URL format or left blank")])
    age = IntegerField('Pet Age', validators=[Optional(), NumberRange(
        min=0, max=30, message="Age must be a whole number from 0 to 30")])
    notes = StringField('Notes', validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form for changing a pet's details"""

    url = StringField('Photo URL', validators=[Optional(), URL(
        require_tld=True, message="Must be a valid URL format or left blank")])
    notes = StringField('Notes', validators=[Optional()])
    available = BooleanField('Available')
