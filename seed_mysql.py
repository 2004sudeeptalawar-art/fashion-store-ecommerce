"""
Seed MySQL Database Script for Fashion Store
Run this script to initialize and seed your MySQL database with all categories, products, variants, and users.

Usage:
  python seed_mysql.py --user root --password YOUR_MYSQL_PASSWORD --host localhost --port 3306 --db fashion_store
"""

import sys
import argparse
import mysql.connector
from config import Config
from models import db, User, Category, Product, ProductVariant, Review, Address
from seed_data import seed_database
from flask import Flask

def init_and_seed_mysql(user, password, host="localhost", port=3306, db_name="fashion_store"):
    print(f"Connecting to MySQL ({host}:{port}) as '{user}'...")
    
    # 1. Create database if it doesn't exist
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, port=port)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[OK] MySQL Database '{db_name}' is ready.")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MySQL: {e}")
        print("\nPlease verify your MySQL password and ensure the MySQL service is running.")
        return False

    from urllib.parse import quote_plus
    encoded_password = quote_plus(password)
    mysql_uri = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{db_name}"
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        print("Creating all tables in MySQL...")
        db.create_all()
        print("Seeding MySQL with luxury fashion catalog...")
        seed_database()
        print("[OK] SUCCESS! MySQL database has been fully populated with all tables and records.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MySQL database for Fashion Store")
    parser.add_argument("--user", default="root", help="MySQL username (default: root)")
    parser.add_argument("--password", required=True, help="MySQL password")
    parser.add_argument("--host", default="localhost", help="MySQL host (default: localhost)")
    parser.add_argument("--port", type=int, default=3306, help="MySQL port (default: 3306)")
    parser.add_argument("--db", default="fashion_store", help="MySQL database name (default: fashion_store)")

    args = parser.parse_args()
    init_and_seed_mysql(args.user, args.password, args.host, args.port, args.db)
