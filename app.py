from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # We actually don't need this but, we do it to have no warnings at console

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

##########################################################
# For every entity (table) that we want in our database
# we are going to make a Class and pass extend it from the db.Model 
# parent object which contains all the previous configuration.
#
# db.Column creates a column/attribute for our table

# Product Model / Entity
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Auto-increment attribute by default
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        # Specifying the fields we want to be available to the user (not to hide)
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init Schema
product_schema = ProductSchema() # If not set to 'True' the console will warn us
products_schema = ProductSchema(many=True) # This init is for when we want to fetch several products (a list)

##########################################

# Route: Create a Product 
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    
    db.session.add(new_product)
    db.session.commit()

    # We use product_schema 'cause we're only adding 1 product
    return product_schema.jsonify(new_product) 

# Route: Get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Route: Get a single product (query parameter <id>)
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Route: Update a Product 
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    # We use product_schema 'cause we're only adding 1 product
    return product_schema.jsonify(product) 

# Route: Delete product (query parameter <id>)
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    print(product)
    db.session.delete(product)
    db.session.commit()

    return 'Product Deleted'

# Run Server (By default it's running on PORT 5000)
if __name__ == '__main__':
    app.run(debug=True)