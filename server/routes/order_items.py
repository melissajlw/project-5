from flask import request, session, jsonify, make_response
from config import db, api
from flask_restful import Resource
from models.models import Order, Product 

class AdminOrders(Resource):
    def get(self):
        orders_data = []
        orders = Order.query.all()
        for order in orders:
            for order_item in order.order_items:
                order_info = {}
                order_info['product_name'] = order_item.product.name
                order_info['total_price'] = order.total_price
                order_info['user_id'] = order.user_id
                order_info['quantity'] = order_item.quantity
                order_info['status'] = order.status
                order_info['order_id'] = order_item.order_id
                product_price = order_item.product.price
                order_info['product_price'] = product_price
                product_id = order_item.product.id
                order_info['product_id'] = product_id
                orders_data.append(order_info)
        return jsonify(orders_data)

api.add_resource(AdminOrders, '/adminOrders')
    
class AdminProducts(Resource):
    def get(self):
        products = [product.to_dict(only=('id', 'name', 'description', 'price', 'image_url','quantity_available',)) for product in Product.query.all()]
        return make_response(products,200)
    
    def post(self):
        data = request.json

        new_product = Product(
            name = data["name"],
            price = data["price"],
            description = data["description"],
            image_url = data['image_url'],
            quantity_available = data['quantity_available'],
            seller_id = 1
        )

        db.session.add(new_product)
        db.session.commit()

        return make_response(jsonify(new_product.to_dict()),200)

api.add_resource(AdminProducts, "/adminProducts")
    
class AdminProductID(Resource):

    def patch(self,id):

        data = request.get_json()

        product = Product.query.filter(Product.id == id).first()

        for attr in data:

            setattr(product,attr,data.get(attr))   

        db.session.add(product)
        db.session.commit()

        return make_response(product.to_dict(),200)

    def delete(self,id):

        product = Product.query.filter(Product.id == id).first()

        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response("",204)
        
        else:
            return make_response(jsonify({"error":"Product not found."}),404)

api.add_resource(AdminProductID,"/adminProducts/<int:id>")