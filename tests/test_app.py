import os
import sys
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Category, Product, ProductVariant, Cart, CartItem, Order, Address

class FashionStoreTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from seed_data import seed_database
            seed_database()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test homepage renders successfully with categories and hero."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ATELIER &amp; CO.", response.data)
        self.assertIn(b"The Art of", response.data)

    def test_catalog_and_filtering(self):
        """Test catalog page, category filter, and search."""
        # Catalog main page
        res = self.client.get('/products')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"The Couture Gallery", res.data)

        # Filter by category
        res_cat = self.client.get('/products?category=womens-collection')
        self.assertEqual(res_cat.status_code, 200)
        self.assertIn(b"L&#39;\xc3\x89toile Velvet Evening Gown", res_cat.data)

        # Search query
        res_search = self.client.get('/products?q=Tuxedo')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b"Savile Structured Wool Tuxedo", res_search.data)

    def test_product_detail_page(self):
        """Test product details and quickview API."""
        with app.app_context():
            prod = Product.query.first()
            pid = prod.product_id

        res = self.client.get(f'/product/{pid}')
        self.assertEqual(res.status_code, 200)

        # Test QuickView JSON API
        res_api = self.client.get(f'/api/product/{pid}/quickview')
        self.assertEqual(res_api.status_code, 200)
        data = json.loads(res_api.data)
        self.assertEqual(data['product_id'], pid)
        self.assertTrue(len(data['variants']) > 0)

    def test_cart_workflow(self):
        """Test adding item to cart, updating quantity, and cart drawer API."""
        with app.app_context():
            variant = ProductVariant.query.first()
            vid = variant.variant_id

        # 1. Add to cart via JSON API
        res_add = self.client.post('/api/cart/add', 
            data=json.dumps({'variant_id': vid, 'quantity': 2}),
            content_type='application/json'
        )
        self.assertEqual(res_add.status_code, 200)
        data_add = json.loads(res_add.data)
        self.assertTrue(data_add['success'])
        self.assertEqual(data_add['cart_count'], 2)

        # 2. Check Drawer API
        res_drawer = self.client.get('/api/cart/drawer')
        self.assertEqual(res_drawer.status_code, 200)
        drawer_data = json.loads(res_drawer.data)
        self.assertEqual(len(drawer_data['items']), 1)
        cart_item_id = drawer_data['items'][0]['cart_item_id']

        # 3. Update quantity
        res_update = self.client.post('/api/cart/update',
            data=json.dumps({'cart_item_id': cart_item_id, 'quantity': 3}),
            content_type='application/json'
        )
        self.assertEqual(res_update.status_code, 200)
        update_data = json.loads(res_update.data)
        self.assertEqual(update_data['cart_count'], 3)

        # 4. View Cart Page
        res_cart = self.client.get('/cart')
        self.assertEqual(res_cart.status_code, 200)
        self.assertIn(b"Your Shopping Bag", res_cart.data)

    def test_user_authentication_flow(self):
        """Test registration, login, profile view, and logout."""
        # 1. Registration
        res_reg = self.client.post('/register', data={
            'full_name': 'Camille Rowe',
            'email': 'camille@vogue.paris',
            'phone': '+33 612345678',
            'password': 'secretpassword',
            'confirm_password': 'secretpassword'
        }, follow_redirects=True)
        self.assertEqual(res_reg.status_code, 200)

        # 2. View Profile
        res_profile = self.client.get('/profile')
        self.assertEqual(res_profile.status_code, 200)
        self.assertIn(b"Camille Rowe", res_profile.data)

        # 3. Logout
        res_logout = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)

        # 4. Login
        res_login = self.client.post('/login', data={
            'email': 'camille@vogue.paris',
            'password': 'secretpassword'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Welcome back", res_login.data)

    def test_checkout_and_order_placement(self):
        """Test adding item and completing checkout order."""
        # Login first
        self.client.post('/login', data={
            'email': 'sophia@example.com',
            'password': 'user123'
        }, follow_redirects=True)

        with app.app_context():
            variant = ProductVariant.query.first()
            vid = variant.variant_id
            addr = Address.query.first()
            aid = addr.address_id

        # Add to cart
        self.client.post('/api/cart/add', 
            data=json.dumps({'variant_id': vid, 'quantity': 1}),
            content_type='application/json'
        )

        # GET Checkout page
        res_check_get = self.client.get('/checkout')
        self.assertEqual(res_check_get.status_code, 200)
        self.assertIn(b"Atelier Checkout", res_check_get.data)

        # POST Checkout to place order
        res_place = self.client.post('/checkout', data={
            'address_id': aid,
            'payment_method': 'Cash on Delivery'
        }, follow_redirects=True)
        self.assertEqual(res_place.status_code, 200)
        self.assertIn(b"ORDER CONFIRMED", res_place.data)

        # Check Order History page
        res_orders = self.client.get('/orders')
        self.assertEqual(res_orders.status_code, 200)
        self.assertIn(b"My Orders", res_orders.data)
        self.assertIn(b"ORD-", res_orders.data)

    def test_admin_dashboard(self):
        """Test admin dashboard access for admin user."""
        # Login as Admin
        self.client.post('/login', data={
            'email': 'admin@vogue.com',
            'password': 'admin123'
        }, follow_redirects=True)

        res_admin = self.client.get('/admin')
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b"Atelier Operations Center", res_admin.data)
        self.assertIn(b"Total Atelier Revenue", res_admin.data)

if __name__ == '__main__':
    unittest.main()
