import os
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vogue-luxe-ultra-secure-key-2026-fashion-store')
    
    # MySQL Database Configuration
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Root@12345')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'fashion_store')
    
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif DB_USER and DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Fallback zero-configuration SQLite for instant out-of-the-box operation
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'fashion_store.db'}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Store settings
    STORE_NAME = "ATELIER & CO."
    STORE_TAGLINE = "High Fashion & Modern Luxury Ready-to-Wear"
    CURRENCY_SYMBOL = "₹"
    FREE_SHIPPING_THRESHOLD = 999.00
    STANDARD_SHIPPING_FEE = 99.00
    TAX_RATE = 0.05 # 5% GST/Tax
