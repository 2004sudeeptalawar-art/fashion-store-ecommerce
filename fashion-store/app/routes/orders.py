from flask import Blueprint, request, jsonify
from app.models.order import Order
from app import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    })