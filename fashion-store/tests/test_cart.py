import unittest
from app import create_app, db
from app.models import User, Product, Order

class CartTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user and product
        self.user = User(username='testuser', email='test@example.com', password='password')
        self.product = Product(name='Test Product', description='Test Description', price=10.00)
        db.session.add(self.user)
        db.session.add(self.product)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_to_cart(self):
        # Simulate adding a product to the cart
        response = self.app.test_client().post('/add_to_cart', json={
            'variant_id': self.product.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Added to cart!', response.data)

    def test_remove_from_cart(self):
        # Simulate removing a product from the cart
        self.app.test_client().post('/add_to_cart', json={
            'variant_id': self.product.id,
            'quantity': 1
        })
        response = self.app.test_client().post('/remove_from_cart', json={
            'variant_id': self.product.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Removed from cart!', response.data)

if __name__ == '__main__':
    unittest.main()