from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models import db, Category, Product, Image, init_db
import logging

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:password@localhost:5432/flaskdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def home():
    return "Welcome"

# Routes for Categories
@app.route("/categories", methods=["GET"])
def list_categories():
    try:
        categories = Category.query.order_by(Category.name).all()
        if not categories:
            return jsonify({"message": "No categories found"}), 404
        category_list = [{"category_id": category.id, "category_name": category.name} for category in categories]
        return jsonify(category_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/category", methods=["POST"])
def add_category():
    try:
        data = request.json
        if not data or not data.get('name'):
            return jsonify({"message": "Category name is required"}), 400
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created", "category_id": new_category.id, "category_name": new_category.name}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Routes for Products
@app.route("/products", methods=["GET"])
def list_products():
    try:
        products = Product.query.order_by(Product.name).all()
        product_list = []
        for product in products:
            category = Category.query.get(product.category_id)
            images = Image.query.filter_by(product_id=product.id).all()
            image_urls = [image.url for image in images]
            product_info = {
                "product_id": product.id,
                "product_name": product.name,
                "price": product.price,
                "category_id": category.id if category else None,
                "category_name": category.name if category else None,
                "image_urls": image_urls
            }
            product_list.append(product_info)
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/product", methods=["POST"])
def add_product():
    try:
        data = request.json
        if not data or not data.get('name') or not data.get('price') or not data.get('category_name'):
            return jsonify({"message": "Product name, price, and category name are required"}), 400

        category_name = data['category_name']
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        new_product = Product(
            name=data['name'],
            price=data['price'],
            category_id=category.id
        )
        db.session.add(new_product)
        db.session.commit()

        if data.get('image_url'):
            new_image = Image(url=data['image_url'], product_id=new_product.id)
            db.session.add(new_image)
            db.session.commit()

        return jsonify({'message': "Product created", "product_id": new_product.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with app.app_context():
        init_db(app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(port=5000)
