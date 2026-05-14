from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    product_id = db.Column(db.Integer)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    product_id = db.Column(db.Integer)
    status = db.Column(db.String(50), default="Pending")


@app.route("/")
def home():
    return jsonify({"message": "ShopRich API running"})


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price}
        for p in products
    ])


@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    product = Product(
        name=data["name"],
        price=data["price"]
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added"})


@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.json
    cart = Cart(
        username=data["username"],
        product_id=data["product_id"]
    )
    db.session.add(cart)
    db.session.commit()
    return jsonify({"message": "Added to cart"})


@app.route("/order", methods=["POST"])
def create_order():
    data = request.json
    order = Order(
        username=data["username"],
        product_id=data["product_id"]
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order placed"})


@app.route("/orders/<username>", methods=["GET"])
def get_orders(username):
    orders = Order.query.filter_by(username=username).all()
    return jsonify([
        {
            "id": o.id,
            "product_id": o.product_id,
            "status": o.status
        }
        for o in orders
    ])


with app.app_context():
    db.create_all()

app.run(host="0.0.0.0", port=5000)
