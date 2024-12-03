from flask import request, session, jsonify, make_response
from config import db, api
from flask_restful import Resource
from models.models import Order, OrderItem

class Orders(Resource):
    def get(self):
        orders = Order.query.all()

        aggregated_orders = []
        for order in orders:
            order_details = {
                'order_id': order.id,
                'status': order.status,
                'total_price': float(sum(item.product.price * item.quantity for item in order.order_items)),
                'products': [{
                    'name': item.product.name, 
                    'quantity': item.quantitiy,
                    'image': item.product.image_url,
                    'price': item.product.price
                    } for item in order.order_items]
            }
            aggregated_orders.append(order_details)

        return make_response(aggregated_orders, 200)
        
    def post(self):
        data = request.get_json()
        current_user_id = session["user_id"]

        try:
            new_order = Order(
                user_id = current_user_id,
                total_price = data["total"],
                status="pending"
            )

            for item in data["items"]:
                order_item = OrderItem(
                    product_id = item["id"],
                    quantity = item["quantity"]
                )
                new_order.order_items.append(order_item)

            db.session.add(new_order)
            db.session.commit()

            return make_response(new_order.to_dict(only=("id", "status", "total_price")), 201)
        
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)
        
api.add_resource(Orders, "/orders")