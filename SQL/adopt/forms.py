from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional


class AddPetForm(FlaskForm):
    """Form for adding a pet"""

    pet_name = StringField('Pet Name', validators=[
                           InputRequired(message='Pet name cannot be left blank')])
    species = StringField('Species', validators=[InputRequired(
        message='Pet species cannot be left blank')])
    url = StringField('Photo URL', validators=[Optional()])
    age = StringField('Pet Age', validators=[Optional()])
    notes = StringField('Notes', validators=[Optional()])
