from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm
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
        age = form.age.data or None
        url = Pet.check_url(form.url.data)
        notes = form.notes.data or None

        pet = Pet(name=name, species=species,
                  photo_url=url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)


@app.route('/<pet_id>', methods=['GET', 'POST'])
def pet_display_edit(pet_id):
    """
    GET ROUTE:
    -Show pet details
    -Show form to edit pet details

    POST ROUTE:
    -Validate form
    -If no validation, re-render page
    -If validated:
        -Update the pet data
        -Redirect to the get route for '/<pet_id>'
    """
    form = EditPetForm()

    pet = Pet.query.get_or_404(pet_id)

    if form.validate_on_submit():
        url = Pet.check_url(form.url.data)
        notes = form.notes.data or None
        available = form.available.data

        pet.photo_url = url
        pet.notes = notes
        pet.available = available

        db.session.add(pet)
        db.session.commit()

        return redirect(f'/{pet_id}')
    else:
        return render_template('display_edit_form.html', form=form, pet=pet)
