from app import db
from app.models.product import Product

def test_product_creation():
    product = Product(name="Test Product", description="This is a test product.", price=9.99)
    db.session.add(product)
    db.session.commit()
    
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.description == "This is a test product."
    assert product.price == 9.99

def test_product_retrieval():
    product = Product.query.filter_by(name="Test Product").first()
    
    assert product is not None
    assert product.name == "Test Product"

def test_product_update():
    product = Product.query.filter_by(name="Test Product").first()
    product.price = 19.99
    db.session.commit()
    
    updated_product = Product.query.get(product.id)
    assert updated_product.price == 19.99

def test_product_deletion():
    product = Product.query.filter_by(name="Test Product").first()
    db.session.delete(product)
    db.session.commit()
    
    deleted_product = Product.query.filter_by(name="Test Product").first()
    assert deleted_product is None