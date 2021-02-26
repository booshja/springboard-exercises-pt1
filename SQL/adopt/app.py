from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm
from models import db, connect_db, Pet


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenzarecool121837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """
    GET ROUTE:
    -List pets and their photos and availability, if present
    """
    pets = Pet.query.all()

    return render_template('home.html', pets=pets or None)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """
    GET ROUTE:
    -Show AddPetForm

    POST ROUTE:
    -Validate from
    -If no validation, re-render form
    -If validated:
        -Create the new pet
        -Redirect to the homepage
    """
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        age = form.age.data
        url = form.species.data or None
        notes = form.notes.data or None

        pet = Pet(name=name, species=species,
                  photo_url=url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        flash("New Pet Added!")

        return redirect('/')
    else:
        return render_template('/add', form=form)
