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

@app.route('/api/cupcakes')
def get_cupcakes():
    """ Get data on all cupcakes"""
    
    cupcakes = Cupcake.query.all()
    serialized = [serialize(c) for c in cupcakes]
    
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<cupcake_id>')
def get_cupcake(cupcake_id):
    
    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize(cupcake)
    
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    
    ''' Don't forget to add 'parent' json category '''
    ''' Post new cupcake function '''

    
    flavor = request.json['cupcake']['flavor']
    size = request.json['cupcake']['size']
    rating = request.json['cupcake']['rating']
    image = request.json['cupcake']['image']
    
    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize(new_cupcake)

    return (jsonify(cupcake=serialized), 201)
