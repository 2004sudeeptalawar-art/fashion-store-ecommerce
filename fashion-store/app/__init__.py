from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from app.routes import auth, cart, products, orders

app.register_blueprint(auth.bp)
app.register_blueprint(cart.bp)
app.register_blueprint(products.bp)
app.register_blueprint(orders.bp)