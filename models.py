from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(255), default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    addresses = db.relationship('Address', backref='user', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.category_name}>'


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(220), nullable=False, unique=True)
    subtitle = db.Column(db.String(255), default="Exclusive Designer Collection")
    description = db.Column(db.Text, nullable=False)
    material_info = db.Column(db.String(255), default="100% Premium Pure Cotton / Sustainable Blend")
    care_instructions = db.Column(db.String(255), default="Dry Clean Only / Gentle Machine Wash")
    base_price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    discount_percent = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=False)
    additional_images = db.Column(db.Text, nullable=True)  # JSON or pipe-separated URLs
    badge = db.Column(db.String(50), default="NEW")  # BESTSELLER, TRENDING, LUXE, SALE
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=4.8)
    reviews_count = db.Column(db.Integer, default=12)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='product', lazy=True, cascade="all, delete-orphan")
    wishlists = db.relationship('Wishlist', backref='product', lazy=True, cascade="all, delete-orphan")

    def get_image_list(self):
        images = [self.image_url]
        if self.additional_images:
            extras = [img.strip() for img in self.additional_images.split('|') if img.strip()]
            images.extend(extras)
        return images

    @property
    def in_stock(self):
        return any(v.stock_quantity > 0 for v in self.variants if v.is_available)

    def __repr__(self):
        return f'<Product {self.product_name}>'


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    variant_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    size_label = db.Column(db.String(30), nullable=False)  # S, M, L, XL, XXL, Free
    color = db.Column(db.String(50), nullable=False)       # Obsidian Black, Champagne, etc.
    color_hex = db.Column(db.String(20), default="#1a1a1a")
    sku = db.Column(db.String(100), unique=True, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=15)
    is_available = db.Column(db.Boolean, default=True)

    cart_items = db.relationship('CartItem', backref='variant', lazy=True)

    def __repr__(self):
        return f'<Variant {self.variant_id} - {self.size_label}/{self.color}>'


class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    session_token = db.Column(db.String(100), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self):
        return sum(item.quantity * item.unit_price for item in self.items)

    def __repr__(self):
        return f'<Cart {self.cart_id} - User {self.user_id}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.variant_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    @property
    def item_subtotal(self):
        return self.quantity * self.unit_price

    def __repr__(self):
        return f'<CartItem {self.cart_item_id} (Variant {self.variant_id} x {self.quantity})>'


class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line = db.Column(db.String(255), nullable=False)
    landmark = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    address_type = db.Column(db.String(20), default="Home")

    orders = db.relationship('Order', backref='address', lazy=True)

    def formatted(self):
        return f"{self.address_line}, {self.city}, {self.state} - {self.pincode}"

    def __repr__(self):
        return f'<Address {self.address_id} - {self.full_name}>'


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=True)
    address_snapshot = db.Column(db.Text, nullable=True)  # Snapshot if address changes later
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0)
    delivery_charge = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default="Cash on Delivery")
    payment_status = db.Column(db.String(50), default="Pending")
    order_status = db.Column(db.String(50), default="Order Placed")  # Order Placed, Processing, Shipped, Delivered, Cancelled
    tracking_number = db.Column(db.String(100), nullable=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.order_number} - {self.order_status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    variant_id = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    size_label = db.Column(db.String(30), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.order_item_id} - {self.product_name}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, default=5)
    headline = db.Column(db.String(150), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    verified_purchase = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id} for Product {self.product_id}>'


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='uq_user_product_wishlist'),)

    def __repr__(self):
        return f'<Wishlist User {self.user_id} - Product {self.product_id}>'
