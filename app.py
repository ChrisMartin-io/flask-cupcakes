"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFACTIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


# Serializer
def serialize(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

def search_serialize(search):
    return {
        "term" : search.search
    }

@app.route('/api/cupcakes')
def get_cupcakes():
    """ Get data on all cupcakes"""
    
    cupcakes = Cupcake.query.all()
    serialized = [serialize(c) for c in cupcakes]
    
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<cupcake_id>')
def get_cupcake(cupcake_id):
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize(cupcake)
    
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    
    ''' Don't forget to add 'parent' json category '''
    ''' Post new cupcake function '''
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    
    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def patch_cupcake(cupcake_id):
    """ patch cupcake info with data from request body """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize(cupcake)

    return (jsonify(cupcake=serialized), 200)

@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ delete the cupcake """

    deleted_cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(deleted_cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route('/')
def index():
    """ returns index page """

    return render_template('index.html')

@app.route('/api/cupcakes/search', methods=["POST"])
def search_cupcake():
    """ searches for a cupcake """

    search_term = request.json['search']
    result = Cupcake.query.filter(Cupcake.flavor.like(search_term)).all()
    serialized = search_serialize(result)
    return jsonify(serialized)
