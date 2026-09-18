from flask import Blueprint, request, jsonify, session
from app import db
from app.models.product import Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    variant_id = data.get('variant_id')
    quantity = data.get('quantity')

    if not variant_id or not quantity:
        return jsonify({'error': 'Invalid data'}), 400

    # Here you would typically add the item to the user's cart in the session or database
    # For simplicity, we'll just return a success message
    return jsonify({'message': 'Item added to cart'}), 200

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    variant_id = data.get('variant_id')

    if not variant_id:
        return jsonify({'error': 'Invalid data'}), 400

    # Here you would typically remove the item from the user's cart in the session or database
    return jsonify({'message': 'Item removed from cart'}), 200

@cart_bp.route('/view_cart', methods=['GET'])
def view_cart():
    # Here you would typically retrieve the user's cart from the session or database
    # For simplicity, we'll return a placeholder response
    return jsonify({'cart': []}), 200