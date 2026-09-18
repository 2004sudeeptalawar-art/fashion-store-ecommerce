import unittest
from app import create_app, db
from app.models.order import Order
from app.models.user import User
from app.models.product import Product

class OrderModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', password='password')
        self.product = Product(name='Test Product', description='Test Description', price=10.0)
        db.session.add(self.user)
        db.session.add(self.product)
        db.session.commit()

        self.order = Order(user_id=self.user.id, product_id=self.product.id, quantity=2)
        db.session.add(self.order)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_order_creation(self):
        self.assertIsNotNone(self.order.id)
        self.assertEqual(self.order.user_id, self.user.id)
        self.assertEqual(self.order.product_id, self.product.id)
        self.assertEqual(self.order.quantity, 2)

    def test_order_relationships(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.product.name, 'Test Product')

if __name__ == '__main__':
    unittest.main()