from flask import request, session, jsonify, make_response
from config import db, api
from flask_restful import Resource
from models.models import Product


class Products(Resource):
    def get(self):
        products = [products.to_dict(only=(
            'id',
            'name',
            'description',
            'price',
            'image_url',
            'quantity_available',
            'seller_id'
        )) for products in Product.query.all()]

        return make_response(jsonify(products), 200)

api.add_resource(Products, "/products")