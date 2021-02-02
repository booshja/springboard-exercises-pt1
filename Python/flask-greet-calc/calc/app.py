from flask import Flask, request
import operations

app = Flask(__name__)

MATH_FUNCS = {
    "mult": operations.mult,
    "div": operations.div,
    "add": operations.add,
    "sub": operations.sub
}


@app.route('/add')
def add():
    """Handles addition, returns a string of the answer"""
    a = int(request.args["a"])
    b = int(request.args["b"])
    sum = str(operations.add(a, b))
    return sum


@app.route('/sub')
def subtract():
    """Handles subtraction, returns a string of the answer"""
    a = int(request.args["a"])
    b = int(request.args["b"])
    difference = str(operations.sub(a, b))
    return difference


@app.route('/mult')
def multiply():
    """Handles multiplication, returns a string of the answer"""
    a = int(request.args["a"])
    b = int(request.args["b"])
    product = str(operations.mult(a, b))
    return product


@app.route('/div')
def divide():
    """Handles division, returns a string of the answer"""
    a = int(request.args["a"])
    b = int(request.args["b"])
    quotient = str(int(operations.div(a, b)))
    return quotient


@app.route('/math/<operation>')
def maths(operation):
    a = int(request.args["a"])
    b = int(request.args["b"])
    return str(int(MATH_FUNCS[operation](a, b)))
