from flask import Flask, request
from flask_cors import CORS, cross_origin

import controllers
from init_util import init_db

init_db()
app = Flask(__name__)
cors = CORS(app)


@cross_origin
@app.route("/api/products", methods = ["GET"])
def get_products():
    response = controllers.get_products()
    return response, 200


@cross_origin
@app.route("/api/products/<int:product_id>", methods = ["GET"])
def get_product(product_id):
    response = controllers.get_product(product_id)
    return response, 200


@cross_origin
@app.route("/api/orders", methods=["POST"])
def add_order():
    controllers.add_order(request.json)
    return {},204

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')
