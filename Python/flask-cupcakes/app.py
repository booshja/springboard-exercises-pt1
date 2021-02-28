"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chickenzarecool13872'

connect_db(app)


@app.route('/')
def front_end():
    """
    GET ROUTE:
    -Render an HTML template
    """
    return render_template('home.html')


@app.route('/api/cupcakes')
def return_all_cupcakes():
    """
    GET ROUTE:
    -Get data about all cupcakes
    -Respond with JSON
        - {cupcakes: [{id, flavor, size, rating, image}, . . .] }
    """
    all_cupcakes = [cup.serialize() for cup in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<cup_id>')
def return_one_cupcake(cup_id):
    """
    GET ROUTE:
    -Get data about a single cupcake
    -Respond with JSON
        - {cupcake: {id, flavor, size, rating, image}}
    -Raise a 404 error if the cupcake cannot be found
    """
    cup = Cupcake.query.get_or_404(cup_id)

    return jsonify(cupcake=cup.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """
    POST ROUTE:
    -Create cupcake and add to database
    -Respond with JSON
        - {cupcake: {id, flavor, size, rating, image}}
    """
    flavor = request.json.get('flavor')
    size = request.json.get('size')
    rating = request.json.get('rating')
    image = request.json.get('image')

    new_cup = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cup)
    db.session.commit()

    response_json = jsonify(cupcake=new_cup.serialize())

    return (response_json, 201)


@app.route('/api/cupcakes/<cup_id>', methods=['PATCH'])
def update_cupcake(cup_id):
    """
    PATCH ROUTE:
    -Update cupcake with the id passed in the URL
        -Can assume the entire cupcake object will be passed to front end
    -Should raise 404 error if cupcake cannot be found
    -Respond with JSON
        - {cupcake: {id, flavor, size, rating, image}}
    """
    cup = Cupcake.query.get_or_404(cup_id)
    cup.flavor = request.json.get('flavor', cup.flavor)
    cup.size = request.json.get('size', cup.size)
    cup.rating = request.json.get('rating', cup.rating)
    cup.image = request.json.get('image', cup.image)

    db.session.commit()

    return jsonify(cupcake=cup.serialize())


@app.route('/api/cupcakes/<cup_id>', methods=['DELETE'])
def delete_cupcake(cup_id):
    """
    DELETE ROUTE:
    -Should raise a 404 error if cupcake cannot be found
    -Delete cupcake with the id passed in the URL
    -Respond with JSON
        - {message: "Deleted"}
    """
    cup = Cupcake.query.get_or_404(cup_id)
    db.session.delete(cup)
    db.session.commit()

    return jsonify(message="Deleted")
