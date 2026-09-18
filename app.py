import os
import uuid
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, abort
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Category, Product, ProductVariant, Cart, CartItem, Address, Order, OrderItem, Review, Wishlist
from seed_data import seed_database

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
CORS(app)

# Initialize SQLAlchemy
db.init_app(app)

with app.app_context():
    db.create_all()
    # Auto-seed database if empty
    try:
        seed_database()
    except Exception as e:
        print(f"Seed note: {e}")

# ---------------------------------------------------------
# Helper Functions & Decorators
# ---------------------------------------------------------

def get_current_user():
    """Retrieve the logged in user or None."""
    user_id = session.get('user_id')
    if user_id:
        return db.session.get(User, user_id)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_admin:
            flash("Administrator access required.", "danger")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def get_or_create_cart():
    """Retrieve or create user/session cart."""
    user = get_current_user()
    if user:
        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
        # Merge guest session cart if exists
        guest_token = session.get('cart_token')
        if guest_token:
            guest_cart = Cart.query.filter_by(session_token=guest_token).first()
            if guest_cart and guest_cart.cart_id != cart.cart_id:
                for item in guest_cart.items:
                    existing = CartItem.query.filter_by(cart_id=cart.cart_id, variant_id=item.variant_id).first()
                    if existing:
                        existing.quantity += item.quantity
                    else:
                        new_item = CartItem(
                            cart_id=cart.cart_id,
                            variant_id=item.variant_id,
                            quantity=item.quantity,
                            unit_price=item.unit_price
                        )
                        db.session.add(new_item)
                db.session.delete(guest_cart)
                db.session.commit()
                session.pop('cart_token', None)
        return cart
    else:
        # Guest cart based on session token
        if 'cart_token' not in session:
            session['cart_token'] = str(uuid.uuid4())
        cart_token = session['cart_token']
        cart = Cart.query.filter_by(session_token=cart_token).first()
        if not cart:
            cart = Cart(session_token=cart_token)
            db.session.add(cart)
            db.session.commit()
        return cart

# ---------------------------------------------------------
# Context Processors & Global Template Variables
# ---------------------------------------------------------

@app.context_processor
def inject_global_data():
    user = get_current_user()
    cart = get_or_create_cart()
    cart_count = cart.total_quantity if cart else 0
    wishlist_count = 0
    if user:
        wishlist_count = Wishlist.query.filter_by(user_id=user.id).count()

    categories = Category.query.filter_by(is_active=True).order_by(Category.display_order.asc()).all()

    return {
        'current_user': user,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'categories_list': categories,
        'store_name': app.config.get('STORE_NAME', 'ATELIER & CO.'),
        'store_tagline': app.config.get('STORE_TAGLINE', 'High Fashion & Luxury Ready-to-Wear'),
        'currency_symbol': app.config.get('CURRENCY_SYMBOL', '₹'),
        'free_shipping_threshold': app.config.get('FREE_SHIPPING_THRESHOLD', 999.00),
        'now_year': datetime.utcnow().year
    }

# ---------------------------------------------------------
# Customer Facing Routes
# ---------------------------------------------------------

@app.route("/")
def home():
    """Editorial Luxury Home Page with Hero, Categories, Bestsellers, New Drops, and Reviews."""
    categories = Category.query.filter_by(is_active=True).order_by(Category.display_order.asc()).all()
    featured_products = Product.query.filter_by(is_active=True, is_featured=True).limit(8).all()
    bestsellers = Product.query.filter_by(is_active=True, badge="BESTSELLER").limit(4).all()
    new_arrivals = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(4).all()
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(3).all()

    return render_template(
        "home.html",
        categories=categories,
        featured_products=featured_products,
        bestsellers=bestsellers,
        new_arrivals=new_arrivals,
        recent_reviews=recent_reviews
    )

@app.route("/products")
@app.route("/shop")
def product_catalog():
    """Comprehensive product catalog with search, filter by category, price, badge, and sorting."""
    category_slug = request.args.get('category')
    search_query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'featured')
    badge_filter = request.args.get('badge')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query.filter_by(is_active=True)
    selected_category = None

    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.category_id)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            (Product.product_name.ilike(search_pattern)) |
            (Product.description.ilike(search_pattern)) |
            (Product.subtitle.ilike(search_pattern))
        )

    if badge_filter:
        query = query.filter_by(badge=badge_filter)

    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)

    # Sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.base_price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.base_price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    else: # featured
        query = query.order_by(Product.is_featured.desc(), Product.created_at.desc())

    products = query.all()
    categories = Category.query.filter_by(is_active=True).all()

    # User wishlist product IDs for active heart icons
    user = get_current_user()
    user_wishlist_pids = set()
    if user:
        user_wishlist_pids = {w.product_id for w in Wishlist.query.filter_by(user_id=user.id).all()}

    return render_template(
        "product_list.html",
        products=products,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        sort_by=sort_by,
        badge_filter=badge_filter,
        user_wishlist_pids=user_wishlist_pids,
        product_count=len(products)
    )

@app.route("/category/<int:cat_id>")
def category_by_id(cat_id):
    cat = Category.query.get_or_404(cat_id)
    return redirect(url_for('product_catalog', category=cat.slug))

@app.route("/product/<int:pid>")
def product_detail(pid):
    """Detailed luxury product view with images, variants, stock, size guide, reviews, and related items."""
    product = Product.query.get_or_404(pid)
    variants = ProductVariant.query.filter_by(product_id=product.product_id, is_available=True).all()
    reviews = Review.query.filter_by(product_id=product.product_id).order_by(Review.created_at.desc()).all()
    
    # Related products in same category
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.product_id != product.product_id,
        Product.is_active == True
    ).limit(4).all()

    user = get_current_user()
    is_in_wishlist = False
    if user:
        is_in_wishlist = Wishlist.query.filter_by(user_id=user.id, product_id=product.product_id).first() is not None

    # Distinct sizes and colors for variant picker
    sizes = []
    colors = []
    for v in variants:
        if v.size_label not in sizes:
            sizes.append(v.size_label)
        color_item = {'name': v.color, 'hex': v.color_hex}
        if color_item not in colors:
            colors.append(color_item)

    return render_template(
        "product_detail.html",
        product=product,
        variants=variants,
        sizes=sizes,
        colors=colors,
        reviews=reviews,
        related_products=related_products,
        is_in_wishlist=is_in_wishlist
    )

# ---------------------------------------------------------
# Cart & Checkout Routes
# ---------------------------------------------------------

@app.route("/cart")
def view_cart():
    """Modern Cart Page with shipping meter, quantity controls, and summary."""
    cart = get_or_create_cart()
    items = cart.items if cart else []
    
    subtotal = sum(item.item_subtotal for item in items)
    free_shipping_limit = app.config.get('FREE_SHIPPING_THRESHOLD', 999.00)
    
    delivery_charge = 0.00 if (subtotal >= free_shipping_limit or subtotal == 0) else app.config.get('STANDARD_SHIPPING_FEE', 99.00)
    tax_amount = round(subtotal * app.config.get('TAX_RATE', 0.05), 2)
    grand_total = round(subtotal + delivery_charge + tax_amount, 2)
    
    free_shipping_progress = min(100, int((subtotal / free_shipping_limit) * 100)) if free_shipping_limit > 0 else 100
    free_shipping_remaining = max(0.00, free_shipping_limit - subtotal)

    return render_template(
        "cart.html",
        cart=cart,
        items=items,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        tax_amount=tax_amount,
        grand_total=grand_total,
        free_shipping_progress=free_shipping_progress,
        free_shipping_remaining=free_shipping_remaining
    )

@app.route("/add_to_cart", methods=["POST"])
@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    """Add a product variant to the cart via AJAX or form."""
    cart = get_or_create_cart()

    if request.is_json:
        data = request.get_json()
        variant_id = data.get("variant_id")
        quantity = int(data.get("quantity", 1))
    else:
        variant_id = request.form.get("variant_id")
        quantity = int(request.form.get("quantity", 1))

    if not variant_id:
        if request.is_json:
            return jsonify({"success": False, "message": "Please select a size and color option."}), 400
        flash("Please select a valid product variant.", "warning")
        return redirect(request.referrer or url_for('view_cart'))

    variant = db.session.get(ProductVariant, variant_id)
    if not variant or not variant.is_available:
        if request.is_json:
            return jsonify({"success": False, "message": "This variant is currently out of stock."}), 400
        flash("Variant unavailable.", "error")
        return redirect(request.referrer or url_for('view_cart'))

    # Check or create cart item
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, variant_id=variant.variant_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.cart_id,
            variant_id=variant.variant_id,
            quantity=quantity,
            unit_price=variant.price
        )
        db.session.add(cart_item)

    db.session.commit()

    if request.is_json:
        return jsonify({
            "success": True,
            "message": f"Added {variant.product.product_name} ({variant.size_label}/{variant.color}) to your shopping bag.",
            "cart_count": cart.total_quantity,
            "cart_subtotal": cart.subtotal
        })

    flash(f"Added {variant.product.product_name} to cart.", "success")
    return redirect(url_for('view_cart'))

@app.route("/update_cart", methods=["POST"])
@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    """Update cart item quantity or delete."""
    cart = get_or_create_cart()

    if request.is_json:
        data = request.get_json()
        item_id = data.get("cart_item_id")
        quantity = int(data.get("quantity", 1))

        item = CartItem.query.filter_by(cart_item_id=item_id, cart_id=cart.cart_id).first()
        if not item:
            return jsonify({"success": False, "message": "Item not found"}), 404

        if quantity <= 0:
            db.session.delete(item)
        else:
            item.quantity = quantity
        db.session.commit()

        # Recalculate summary
        subtotal = cart.subtotal
        free_limit = app.config.get('FREE_SHIPPING_THRESHOLD', 999.00)
        shipping = 0.00 if (subtotal >= free_limit or subtotal == 0) else app.config.get('STANDARD_SHIPPING_FEE', 99.00)
        tax = round(subtotal * app.config.get('TAX_RATE', 0.05), 2)
        grand_total = round(subtotal + shipping + tax, 2)

        return jsonify({
            "success": True,
            "cart_count": cart.total_quantity,
            "subtotal": subtotal,
            "shipping": shipping,
            "tax": tax,
            "grand_total": grand_total,
            "item_subtotal": item.item_subtotal if quantity > 0 else 0
        })

    # Form post handling
    for key, value in request.form.items():
        if key.startswith("item_"):
            try:
                item_id = int(key.split("_")[1])
                qty = int(value)
                item = CartItem.query.filter_by(cart_item_id=item_id, cart_id=cart.cart_id).first()
                if item:
                    if qty <= 0:
                        db.session.delete(item)
                    else:
                        item.quantity = qty
            except ValueError:
                continue

    db.session.commit()
    flash("Cart updated successfully.", "success")
    return redirect(url_for('view_cart'))

@app.route("/cart/remove/<int:item_id>", methods=["POST", "GET"])
def remove_cart_item(item_id):
    """Remove a specific item from cart."""
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_item_id=item_id, cart_id=cart.cart_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        if request.is_json:
            return jsonify({"success": True, "cart_count": cart.total_quantity, "cart_subtotal": cart.subtotal})
        flash("Item removed from your cart.", "info")
    return redirect(url_for('view_cart'))

@app.route("/api/cart/drawer")
def cart_drawer_data():
    """Return JSON representation of cart for live slide-over drawer."""
    cart = get_or_create_cart()
    items_data = []
    if cart:
        for it in cart.items:
            items_data.append({
                "cart_item_id": it.cart_item_id,
                "product_id": it.variant.product.product_id,
                "product_name": it.variant.product.product_name,
                "image_url": it.variant.product.image_url,
                "size": it.variant.size_label,
                "color": it.variant.color,
                "price": it.unit_price,
                "quantity": it.quantity,
                "subtotal": it.item_subtotal
            })

    subtotal = cart.subtotal if cart else 0
    free_limit = app.config.get('FREE_SHIPPING_THRESHOLD', 999.00)

    return jsonify({
        "items": items_data,
        "total_quantity": cart.total_quantity if cart else 0,
        "subtotal": subtotal,
        "free_shipping_threshold": free_limit,
        "free_shipping_remaining": max(0.00, free_limit - subtotal),
        "free_shipping_progress": min(100, int((subtotal / free_limit) * 100)) if free_limit > 0 else 100
    })

# ---------------------------------------------------------
# Checkout & Orders
# ---------------------------------------------------------

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """Streamlined Checkout Flow with Saved Addresses and Live Order Calculation."""
    user = get_current_user()
    cart = get_or_create_cart()
    items = cart.items if cart else []

    if not items:
        flash("Your shopping cart is currently empty.", "warning")
        return redirect(url_for('product_catalog'))

    subtotal = sum(it.item_subtotal for it in items)
    free_limit = app.config.get('FREE_SHIPPING_THRESHOLD', 999.00)
    delivery_charge = 0.00 if (subtotal >= free_limit or subtotal == 0) else app.config.get('STANDARD_SHIPPING_FEE', 99.00)
    tax_amount = round(subtotal * app.config.get('TAX_RATE', 0.05), 2)
    grand_total = round(subtotal + delivery_charge + tax_amount, 2)

    addresses = Address.query.filter_by(user_id=user.id).all()

    if request.method == "POST":
        address_id = request.form.get('address_id')
        payment_method = request.form.get('payment_method', 'Cash on Delivery')

        # Check if user added a new address directly on checkout
        if not address_id or address_id == "new":
            full_name = request.form.get('full_name', user.full_name)
            phone = request.form.get('phone', user.phone or '0000000000')
            address_line = request.form.get('address_line')
            city = request.form.get('city')
            state = request.form.get('state')
            pincode = request.form.get('pincode')

            if not address_line or not city or not pincode:
                flash("Please select an address or complete all required delivery address fields.", "danger")
                return redirect(url_for('checkout'))

            new_addr = Address(
                user_id=user.id,
                full_name=full_name,
                phone=phone,
                address_line=address_line,
                city=city,
                state=state or 'Default State',
                pincode=pincode,
                is_default=(len(addresses) == 0)
            )
            db.session.add(new_addr)
            db.session.flush()
            selected_address = new_addr
        else:
            selected_address = Address.query.filter_by(address_id=address_id, user_id=user.id).first()
            if not selected_address:
                flash("Please choose a valid delivery address.", "warning")
                return redirect(url_for('checkout'))

        # Create Order
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        tracking_no = f"TRK-{uuid.uuid4().hex[:8].upper()}"

        order = Order(
            order_number=order_number,
            user_id=user.id,
            address_id=selected_address.address_id,
            address_snapshot=f"{selected_address.full_name}, {selected_address.phone}, {selected_address.formatted()}",
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_charge=delivery_charge,
            discount_amount=0.00,
            total_amount=grand_total,
            payment_method=payment_method,
            payment_status="Paid" if payment_method != "Cash on Delivery" else "Pending",
            order_status="Order Placed",
            tracking_number=tracking_no
        )
        db.session.add(order)
        db.session.flush()

        # Create Order Items and decrease stock
        for it in items:
            order_item = OrderItem(
                order_id=order.order_id,
                variant_id=it.variant_id,
                product_id=it.variant.product_id,
                product_name=it.variant.product.product_name,
                size_label=it.variant.size_label,
                color=it.variant.color,
                image_url=it.variant.product.image_url,
                unit_price=it.unit_price,
                quantity=it.quantity,
                subtotal=it.item_subtotal
            )
            db.session.add(order_item)

            # Reduce variant inventory stock
            if it.variant.stock_quantity >= it.quantity:
                it.variant.stock_quantity -= it.quantity

        # Clear the Cart
        for it in items:
            db.session.delete(it)

        db.session.commit()

        flash(f"Order #{order_number} confirmed! Thank you for shopping with us.", "success")
        return redirect(url_for('order_success', order_number=order_number))

    return render_template(
        "checkout.html",
        cart_items=items,
        addresses=addresses,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        tax_amount=tax_amount,
        grand_total=grand_total
    )

@app.route("/order/confirmation/<order_number>")
@login_required
def order_success(order_number):
    """Order confirmation and instant receipt screen."""
    user = get_current_user()
    order = Order.query.filter_by(order_number=order_number, user_id=user.id).first_or_404()
    return render_template("order_details.html", order=order, items=order.items, is_confirmation=True)

@app.route("/orders")
@login_required
def orders():
    """User Order History."""
    user = get_current_user()
    user_orders = Order.query.filter_by(user_id=user.id).order_by(Order.order_date.desc()).all()
    return render_template("orders.html", orders=user_orders)

@app.route("/order/<int:oid>")
@app.route("/order/track/<order_number>")
@login_required
def order_details(oid=None, order_number=None):
    """View detailed order status with tracking progress bar and printable invoice."""
    user = get_current_user()
    if oid:
        order = Order.query.filter_by(order_id=oid, user_id=user.id).first_or_404()
    else:
        order = Order.query.filter_by(order_number=order_number, user_id=user.id).first_or_404()
    return render_template("order_details.html", order=order, items=order.items, is_confirmation=False)

# ---------------------------------------------------------
# Wishlist
# ---------------------------------------------------------

@app.route("/wishlist")
@login_required
def wishlist():
    """User wishlist view."""
    user = get_current_user()
    wishlist_items = Wishlist.query.filter_by(user_id=user.id).order_by(Wishlist.created_at.desc()).all()
    products = [w.product for w in wishlist_items if w.product]
    return render_template("wishlist.html", products=products)

@app.route("/api/wishlist/toggle", methods=["POST"])
def toggle_wishlist():
    """Toggle item in wishlist via AJAX."""
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "require_login": True, "message": "Please log in to save to your wishlist."}), 401

    data = request.get_json() or {}
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({"success": False, "message": "Invalid product"}), 400

    existing = Wishlist.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        added = False
        msg = "Removed from wishlist"
    else:
        new_w = Wishlist(user_id=user.id, product_id=product_id)
        db.session.add(new_w)
        db.session.commit()
        added = True
        msg = "Added to wishlist"

    count = Wishlist.query.filter_by(user_id=user.id).count()
    return jsonify({"success": True, "added": added, "message": msg, "wishlist_count": count})

# ---------------------------------------------------------
# Product Quick View API
# ---------------------------------------------------------

@app.route("/api/product/<int:pid>/quickview")
def api_product_quickview(pid):
    """Return JSON for dynamic quick view modal."""
    product = Product.query.get_or_404(pid)
    variants = ProductVariant.query.filter_by(product_id=product.product_id, is_available=True).all()
    
    variant_data = []
    for v in variants:
        variant_data.append({
            "variant_id": v.variant_id,
            "size": v.size_label,
            "color": v.color,
            "color_hex": v.color_hex,
            "price": v.price,
            "stock": v.stock_quantity
        })

    return jsonify({
        "product_id": product.product_id,
        "product_name": product.product_name,
        "subtitle": product.subtitle,
        "description": product.description,
        "material": product.material_info,
        "base_price": product.base_price,
        "original_price": product.original_price,
        "discount_percent": product.discount_percent,
        "rating": product.rating,
        "reviews_count": product.reviews_count,
        "image_url": product.image_url,
        "images": product.get_image_list(),
        "variants": variant_data
    })

# ---------------------------------------------------------
# Customer Reviews
# ---------------------------------------------------------

@app.route("/product/<int:pid>/review", methods=["POST"])
@login_required
def add_review(pid):
    """Add a customer rating & review."""
    user = get_current_user()
    product = Product.query.get_or_404(pid)
    
    rating = int(request.form.get('rating', 5))
    headline = request.form.get('headline', '').strip()
    comment = request.form.get('comment', '').strip()

    if not comment:
        flash("Please write a short review comment.", "warning")
        return redirect(url_for('product_detail', pid=pid))

    review = Review(
        product_id=product.product_id,
        user_id=user.id,
        user_name=user.full_name,
        rating=rating,
        headline=headline,
        comment=comment,
        verified_purchase=True
    )
    db.session.add(review)
    
    # Update aggregate product rating
    all_reviews = Review.query.filter_by(product_id=product.product_id).all()
    total_ratings = sum(r.rating for r in all_reviews) + rating
    product.reviews_count = len(all_reviews) + 1
    product.rating = round(total_ratings / product.reviews_count, 1)

    db.session.commit()
    flash("Thank you! Your review has been published.", "success")
    return redirect(url_for('product_detail', pid=pid))

# ---------------------------------------------------------
# Authentication & User Management
# ---------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == "POST":
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email address already exists. Please sign in.", "warning")
            return redirect(url_for('login'))

        user = User(
            full_name=full_name,
            email=email,
            phone=phone
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Log user in
        session['user_id'] = user.id
        flash(f"Welcome to {app.config.get('STORE_NAME')}, {user.full_name}!", "success")
        return redirect(url_for('home'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User Login."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    next_page = request.args.get('next')

    if request.method == "POST":
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f"Welcome back, {user.full_name}!", "success")
            if next_page and not next_page.startswith('http'):
                return redirect(next_page)
            return redirect(url_for('admin_dashboard') if user.is_admin else url_for('home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """User Logout."""
    session.pop('user_id', None)
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('home'))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User Profile Page."""
    user = get_current_user()
    if request.method == "POST":
        user.full_name = request.form.get('full_name', user.full_name)
        user.phone = request.form.get('phone', user.phone)
        
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
            flash("Password updated successfully.", "success")

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile'))

    recent_orders = Order.query.filter_by(user_id=user.id).order_by(Order.order_date.desc()).limit(5).all()
    addresses = Address.query.filter_by(user_id=user.id).all()
    return render_template("profile.html", user=user, recent_orders=recent_orders, addresses=addresses)

@app.route("/addresses", methods=["GET", "POST"])
@login_required
def manage_addresses():
    """User Address Book."""
    user = get_current_user()
    if request.method == "POST":
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address_line = request.form.get('address_line')
        landmark = request.form.get('landmark', '')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        address_type = request.form.get('address_type', 'Home')
        is_default = bool(request.form.get('is_default'))

        if is_default:
            Address.query.filter_by(user_id=user.id).update({'is_default': False})

        new_addr = Address(
            user_id=user.id,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            landmark=landmark,
            city=city,
            state=state,
            pincode=pincode,
            address_type=address_type,
            is_default=is_default
        )
        db.session.add(new_addr)
        db.session.commit()
        flash("Delivery address saved.", "success")
        return redirect(url_for('manage_addresses'))

    addresses = Address.query.filter_by(user_id=user.id).all()
    return render_template("addresses.html", addresses=addresses)

@app.route("/addresses/delete/<int:aid>", methods=["POST"])
@login_required
def delete_address(aid):
    user = get_current_user()
    addr = Address.query.filter_by(address_id=aid, user_id=user.id).first_or_404()
    db.session.delete(addr)
    db.session.commit()
    flash("Address deleted.", "info")
    return redirect(url_for('manage_addresses'))

# ---------------------------------------------------------
# Admin Dashboard & Inventory Management
# ---------------------------------------------------------

@app.route("/admin")
@admin_required
def admin_dashboard():
    """Admin Overview & Product/Order Management Hub."""
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_users = User.query.count()
    total_revenue = sum(o.total_amount for o in Order.query.all())

    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()

    return render_template(
        "admin.html",
        total_orders=total_orders,
        total_products=total_products,
        total_users=total_users,
        total_revenue=total_revenue,
        recent_orders=recent_orders,
        products=products,
        categories=categories
    )

@app.route("/admin/product/add", methods=["POST"])
@admin_required
def admin_add_product():
    """Create a new product with default variants."""
    name = request.form.get('product_name')
    cat_id = request.form.get('category_id')
    price = float(request.form.get('base_price', 0))
    desc = request.form.get('description', '')
    img = request.form.get('image_url', 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80')
    badge = request.form.get('badge', 'NEW')
    is_featured = bool(request.form.get('is_featured'))

    slug = name.lower().replace(' ', '-').replace("'", '') + f"-{uuid.uuid4().hex[:4]}"

    product = Product(
        category_id=cat_id,
        product_name=name,
        slug=slug,
        base_price=price,
        description=desc,
        image_url=img,
        badge=badge,
        is_featured=is_featured
    )
    db.session.add(product)
    db.session.flush()

    # Add standard size variants
    for sz in ['S', 'M', 'L', 'XL']:
        variant = ProductVariant(
            product_id=product.product_id,
            size_label=sz,
            color="Standard Color",
            color_hex="#1a1a1a",
            sku=f"SKU-{product.product_id}-{sz}",
            price=price,
            stock_quantity=20,
            is_available=True
        )
        db.session.add(variant)

    db.session.commit()
    flash(f"Product '{name}' created with variants successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/order/status/<int:oid>", methods=["POST"])
@admin_required
def admin_update_order_status(oid):
    """Update order status."""
    order = Order.query.get_or_404(oid)
    new_status = request.form.get('order_status')
    if new_status:
        order.order_status = new_status
        db.session.commit()
        flash(f"Order #{order.order_number} status updated to '{new_status}'.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/product/delete/<int:pid>", methods=["POST"])
@admin_required
def admin_delete_product(pid):
    """Delete a product."""
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for('admin_dashboard'))

# ---------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
