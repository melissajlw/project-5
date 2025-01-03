#!/usr/bin/env python3
from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models.models import User, Seller, Customer, Category, Item, CartItem, OrderItem, Order, Review
import json
from datetime import datetime

app.secret_key=b'\xaf\x88\x87_\x1a\xf4\x97\x93f\xf5q\x0b\xad\xef,\xb3'

def apply_json_loads(item):
    item['prices'] = json.loads(item['prices'])
    item['discount_prices'] = json.loads(item['discount_prices'])
    item['amounts'] = json.loads(item['amounts'])
    item['units'] = json.loads(item['units'])
    item['packs'] = json.loads(item['packs'])
    item['about_item'] = json.loads(item['about_item'])
    item['details_1'] = json.loads(item['details_1'])
    item['details_2'] = json.loads(item['details_2'])
    item['images'] = json.loads(item['images'])
    return item

@app.before_request
def check_if_signed_in():
    if not session.get('user_id') \
        and request.endpoint != 'authenticate' \
        and request.endpoint != 'signup' \
        and not (request.endpoint == 'items' and request.method == 'GET') \
        and not (request.endpoint == 'item_by_id' and request.method == 'GET') \
        and request.endpoint != 'items_by_rating' \
        and request.endpoint != 'items_by_sales' \
        and request.endpoint != 'reviews_by_itemid':
        return make_response({
            'message': 'User is not signed in',
        }, 401)

@app.route('/')
def index():
    return '<h1>Project Home</h1>'

class Authenticate(Resource):
    def get(self):
        user = User.query.filter_by(id=session.get('user_id')).first()
    
        if not user:
            return make_response({
                'message':'User is not logged in.'
            }, 401)
        
        userInfo = user.to_dict()
        if userInfo.get('customer'):
            for item in userInfo['customer']['cart_items']:
                if item.get('item'):
                    apply_json_loads(item['item'])
            
            for order in userInfo['customer']['orders']:
                for order_item in order['order_items']:
                    if order_item.get('item'):
                        apply_json_loads(order_item['item'])

            for review in userInfo['customer']['reviews']:
                if review.get('item'):
                    apply_json_loads(review['item'])
        else:
            for item in userInfo['seller']['items']:
                apply_json_loads(item)
        return make_response(userInfo, 200)
    
    def post(self):
        req = request.get_json()
        user = User.query.filter_by(username=req.get('username')).first()
        print('in Authenticate, user: ', user)
        if user and user.authenticate(req.get('password')):
            print('in Authenticate, authentication successful.')
            session['user_id'] = user.id
            userInfo = user.to_dict()
            if userInfo.get('customer'):
                for item in userInfo['customer']['cart_items']:
                    if item.get('item'):
                        apply_json_loads(item['item'])

                for order in userInfo['customer']['orders']:
                    for order_item in order['order_items']:
                        if order_item.get('item'):
                            apply_json_loads(order_item['item'])

                for review in userInfo['customer']['reviews']:
                    if review.get('item'):
                        apply_json_loads(review['item'])
            else:
                for item in userInfo['seller']['items']:
                    apply_json_loads(item)
            return make_response(userInfo, 200)
        return make_response({
            'message': 'Invalid username or password.'
        }, 401)
    
    def delete(self):
        session['user_id'] = None
        return make_response({}, 204)

api.add_resource(Authenticate, '/authenticate', endpoint='authenticate')

class Signup(Resource):
    def post(self):
        req = request.get_json()
        try: 
            user = User(
                username = req.get('username'),
                password_hash = req.get('password'),
                phone = req.get('phone'),
                email = req.get('email'),
                street_1 = req.get('street_1'),
                street_2 = req.get('street_2'),
                city = req.get('city'),
                state = req.get('state'),
                zip_code = req.get('zipCode'),
            )
            db.session.add(user)

            if req.get('isSeller'):
                seller = Seller(
                    name = req.get('name'),
                    user = user,
                )
                db.session.add(seller)
            else:
                customer = Customer(
                    first_name = req.get('firstName'),
                    last_name = req.get('lastName'),
                    mobile = req.get('mobile'),
                    nickname = req.get('firstName'),
                    user = user,
                )
                db.session.add(customer)
            db.session.commit()
        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        session['user_id'] = user.id
        userInfo = user.to_dict()
        if userInfo.get('customer'):
            for item in userInfo['customer']['cart_items']:
                if item.get('item'):
                    apply_json_loads(item['item'])

            for order in userInfo['customer']['orders']:
                for order_item in order['order_items']:
                    if order_item.get('item'):
                        apply_json_loads(order_item['item'])

            for review in userInfo['customer']['reviews']:
                if review.get('item'):
                    apply_json_loads(review['item'])
        else:
            for item in userInfo['seller']['items']:
                apply_json_loads(item)
        return make_response(userInfo, 201)

api.add_resource(Signup, '/signup', endpoint='signup')
                
class Customer_by_id(Resource):
    def patch(self, id):
        req = request.get_json()
        customer = Customer.query.filter_by(id=id).first()
        if customer: 
            try:
                for key in req:
                    setattr(customer, key, req[key])
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            
            return make_response(customer.to_dict(), 200)
        
        return make_response({
            'message': f'Customer {id} not found.',
        }, 404)

api.add_resource(Customer_by_id, '/customers/<int:id>') 

class Items(Resource): 
    def get(self):
        items = [apply_json_loads(item.to_dict()) for item in Item.query.all() if item.active]
        return make_response(items, 200)

    def post(self):
        req = request.get_json()
        try:
            item = Item(
                active = 1,
                name = req.get('name'),
                brand = req.get('brand'),
                default_item_idx = req.get('default_item_idx'),
                prices = req.get('prices'),
                discount_prices = req.get('discount_prices'),
                amounts = req.get('amounts'),
                units = req.get('units'),
                packs = req.get('packs'),
                about_item = req.get('about_item'),
                details_1 = req.get('details_1'),
                details_2 = req.get('details_2'),
                images = req.get('images'),
                category_id = req.get('category_id'),
                seller_id = req.get('seller_id'),
            )
            db.session.add(item)
            db.session.commit()
        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        return make_response(apply_json_loads(item.to_dict()), 201)

api.add_resource(Items, '/items', endpoint='items')

class Item_by_id(Resource):
    def get(self, id):
        item = Item.query.filter_by(id=id).first()
        if item and item.active: 
            itemInfo = item.to_dict()
            apply_json_loads(itemInfo)
            return make_response(itemInfo, 200)
        return make_response({
            'message': f'Item {id} not found.',
        }, 404)
    
    def patch(self, id):
        req = request.get_json()
        item = Item.query.filter_by(id=id).first()
        if item: 
            try: 
                for key in req:
                    setattr(item, key, req[key])
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            itemInfo = item.to_dict()
            apply_json_loads(itemInfo)
            return make_response(itemInfo, 200)
        
        return make_response({
            'message': f'Item {id} not found.',
        }, 404)


    def delete(self, id):
        item = Item.query.filter_by(id=id).first()
        if item: 
            try: 
                db.session.delete(item)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            return make_response({}, 204)
        
        return make_response({
            'message': f'Item {id} not found.',
        }, 404)

api.add_resource(Item_by_id, '/items/<int:id>', endpoint='item_by_id') 

class Items_by_rating(Resource):
    def get(self):
        items = Item.query.filter(Item.active == 1).order_by(Item.avg_review_rating.desc()).limit(4).all()
        itemInfo = [apply_json_loads(item.to_dict()) for item in items]
        return make_response(itemInfo, 200)

api.add_resource(Items_by_rating, '/items/rating', endpoint='items_by_rating')

class Items_by_sales(Resource):
    def get(self):
        items = Item.query.filter(Item.active == 1).order_by(Item.accum_sales_cnt.desc()).limit(4).all()
        itemInfo = [apply_json_loads(item.to_dict()) for item in items]
        return make_response(itemInfo, 200)

api.add_resource(Items_by_sales, '/items/sales', endpoint='items_by_sales')

class CartItems(Resource):
    def post(self): 
        req = request.get_json()
        try: 
            item = CartItem(
                checked = 1,
                quantity = req.get('quantity'),
                item_idx = req.get('item_idx'),
                item_id = req.get('item_id'),
                customer_id = req.get('customer_id')
            )
            db.session.add(item)
            db.session.commit()
        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        cartItemInfo = item.to_dict()
        if cartItemInfo.get('item'):
            apply_json_loads(cartItemInfo['item'])
        return make_response(cartItemInfo, 201)

api.add_resource(CartItems, '/cartitems', endpoint='cartitems') 

class CartItem_by_id(Resource):
    def patch(self, id):
        req = request.get_json()
        item = CartItem.query.filter_by(id=id).first()
        if item:
            try:
                for key in req:
                    setattr(item, key, req[key])
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            
            cartItemInfo = item.to_dict()
            if cartItemInfo.get('item'):
                apply_json_loads(cartItemInfo['item'])
            return make_response(cartItemInfo, 200)
        
        return make_response({
            'message': f'Cart Item {id} not found.',
        }, 404)
    
    def delete(self, id):
        item = CartItem.query.filter_by(id=id).first()
        if item:
            try:
                db.session.delete(item)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            return make_response({}, 204)
        
        return make_response({
            'message': f'Cart Item {id} not found.',
        }, 404)

api.add_resource(CartItem_by_id, '/cartitems/<int:id>', endpoint='cartitem_by_id')

class Orders(Resource):
    def post(self):
        req = request.get_json()
        try:
            o = Order(
                closed_date = None,
                street_1 = req.get('street_1'),
                street_2 = req.get('street_2'),
                city = req.get('city'),
                state = req.get('state'),
                zip_code = req.get('zip_code'),
                customer_id = req.get('customer_id')
            )
            db.session.add(o)
            db.session.commit()
        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        orderInfo = o.to_dict()
        for order_item in orderInfo['order_items']:
            if order_item.get('item'):
                apply_json_loads(order_item['item'])
        return make_response(orderInfo, 201)

api.add_resource(Orders, '/orders') 

class Order_by_id(Resource):
    def get(self, id):
        o = Order.query.filter_by(id=id).first()
        if o:
            return make_response(o.to_dict(), 200)
        
        return make_response({
            'message': f'Order {id} not found.'
        }, 404) 
    
    def patch(self, id):
        req = request.get_json()
        o = Order.query.filter_by(id=id).first()
        if o:
            try:
                for key in req:
                    if key != 'closed_date':
                        setattr(o, key, req[key])
                    else:
                        d = datetime.strptime(req[key], '%Y-%m-%d %H:%M:%S')
                        setattr(o, key, d)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            
            return make_response(o.to_dict(), 200)
        
        return make_response({
            'message': f'Order {id} not found.'
        })

    def delete(self, id):
        o = Order.query.filter_by(id=id).first()
        if o:
            try:
                db.session.delete(o)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            return make_response({}, 204)

        return make_response({
            'message': f'Order {id} not found.',
        }, 404)

api.add_resource(Order_by_id, '/orders/<int:id>') 

class OrderItems(Resource):
    def post(self):
        req = request.get_json()
        try:
            oi = OrderItem(
                quantity = req.get('quantity'),
                price = req.get('price'),
                processed_date = None,
                item_idx = req.get('item_idx'),
                item_id = req.get('item_id'),
                order_id = req.get('order_id')
            )
            db.session.add(oi)
            db.session.commit()

            item = Item.query.filter_by(id=oi.item_id).first()
            itemInfo = item.to_dict()
            apply_json_loads(itemInfo)
            item.accum_sales_cnt += oi.quantity * itemInfo['packs'][oi.item_idx]
            db.session.add(item)
            db.session.commit()

        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        orderItemInfo = oi.to_dict()
        if orderItemInfo.get('item'):
            apply_json_loads(orderItemInfo['item'])
        return make_response(orderItemInfo, 201)

api.add_resource(OrderItems, '/orderitems') 

class OrderItem_by_id(Resource):
    def patch(self, id):
        req = request.get_json()
        oi = OrderItem.query.filter_by(id=id).first()
        if oi:
            try:
                item_id = oi.item_id
                item = Item.query.filter_by(id=item_id).first()
                itemInfo = item.to_dict()
                apply_json_loads(itemInfo)
                sales_cnt = oi.quantity * itemInfo['packs'][oi.item_idx]

                for key in req:
                    if key != 'processed_date':
                        setattr(oi, key, req[key])
                    else:
                        d = datetime.strptime(req[key], '%Y-%m-%d %H:%M:%S')
                        setattr(oi, key, d)
                db.session.commit()

                if oi.item_id == item_id:
                    updated_sales_cnt = oi.quantity * itemInfo['packs'][oi.item_idx]
                    if updated_sales_cnt != sales_cnt:
                        item.accum_sales_cnt += updated_sales_cnt - sales_cnt
                    db.session.add(item)
                else:
                    new_item = Item.query.filter_by(id=oi.item_id).first()
                    new_item_dict = new_item.to_dict()
                    apply_json_loads(new_item_dict)
                    new_item.accum_sales_cnt += (oi.quantity * new_item_dict['packs'][oi.item_idx])
                    db.session.add(new_item)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)

            return make_response(oi.to_dict(), 200)
        
        return make_response({
            'message': f'OrderItem {id} not found.',
        }, 404)

api.add_resource(OrderItem_by_id, '/orderitems/<int:id>')

    
class Reviews(Resource):
    def post(self):
        req = request.get_json()
        try:
            r = Review(
                rating = req.get('rating'),
                headline = req.get('headline'),
                content = req.get('content'),
                images = req.get('images'),
                review_done = req.get('review_done'),
                item_id = req.get('item_id'),
                customer_id = req.get('customer_id')
            )
            db.session.add(r)
            db.session.commit()

            if r.review_done and (1 <= r.rating <= 5):
                item = Item.query.filter_by(id=r.item_id).first()
                item.accum_review_cnt += 1
                item.avg_review_rating += (r.rating - item.avg_review_rating) / item.accum_review_cnt
                db.session.add(item)
                db.session.commit()
        except Exception as exc:
            return make_response({
                'message': f'{exc}',
            }, 400)
        
        reviewInfo = r.to_dict()
        if reviewInfo.get('item'):
            apply_json_loads(reviewInfo['item'])
        return make_response(reviewInfo, 201)

api.add_resource(Reviews, '/reviews') 

class Review_by_id(Resource):
    def patch(self, id):
        req = request.get_json()
        r = Review.query.filter_by(id=id).first()
        if r:
            try:
                prev_review_done = r.review_done
                prev_rating = r.rating

                for key in req:
                    setattr(r, key, req[key])
                db.session.commit()

                item = Item.query.filter_by(id=r.item_id).first()
                if r.review_done and (1 <= r.rating <= 5):
                    if prev_review_done:
                        if r.rating != prev_rating:
                            item.accum_review_cnt -= 1
                            item.avg_review_rating -= (prev_rating - item.avg_review_rating) / item.accum_review_cnt
                            item.accum_review_cnt += 1
                            item.avg_review_rating += (r.rating - item.avg_review_rating) / item.accum_review_cnt
                            db.session.add(item)
                            db.session.commit()
                    else:
                        item.accum_review_cnt += 1
                        item.avg_review_rating += (r.rating - item.avg_review_rating) / item.accum_review_cnt
                        db.session.add(item)
                        db.session.commit()
                else:
                    if prev_review_done:
                        item.accum_review_cnt -= 1
                        item.avg_review_rating -= (prev_rating - item.avg_review_rating) / item.accum_review_cnt
                        db.session.add(item)
                        db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            
            reviewInfo = r.to_dict()
            if reviewInfo.get('item'):
                apply_json_loads(reviewInfo['item'])
            return make_response(reviewInfo, 200)
        
        return make_response({
            'message': f'Review {id} not found.',
        }, 404)
    
    def delete(self, id):
        r = Review.query.filter_by(id=id).first()
        if r:
            try:
                if r.review_done and (1 <= r.rating <= 5):
                    item = Item.query.filter_by(id=r.item_id).first()
                    item.accum_review_cnt -= 1
                    item.avg_review_rating -= (r.rating - item.avg_review_rating) / item.accum_review_cnt
                    db.session.add(item)

                db.session.delete(r)
                db.session.commit()
            except Exception as exc:
                return make_response({
                    'message': f'{exc}',
                }, 400)
            
            return make_response({}, 204)
        
        return make_response({
            'message': f'Review {id} not found.',
        }, 404)

api.add_resource(Review_by_id, '/reviews/<int:id>')

class Reviews_by_itemId(Resource):
    def get(self, iid):
        itemReviews = [ r.to_dict() for r in Review.query.filter_by(item_id=iid).all()]
        for reviewInfo in itemReviews:
            reviewInfo.pop('item', None)
        return make_response(itemReviews, 200)

api.add_resource(Reviews_by_itemId, '/reviews/items/<int:iid>', endpoint='reviews_by_itemid')

if __name__ == '__main__':
    app.run(port=5555, debug=True)