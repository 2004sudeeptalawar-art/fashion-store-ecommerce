# 👗 Fashion Store - E-Commerce Web Application

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg)](https://www.sqlite.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Compatible-orange.svg)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern, full-featured e-commerce web platform built with Flask and Python. The application enables users to discover, search, and purchase trendy fashion products with an intuitive, responsive user experience.

---

## ✨ Features

- **🛍️ Product Catalog & Filtering**: Browse through diverse categories, search by keywords, filter by price and tags, and view high-resolution product details.
- **🔐 User Authentication**: Secure user registration, login/logout, password encryption, profile management, and saved shipping addresses.
- **🛒 Interactive Shopping Cart**: Add items, update quantities dynamically, and calculate order totals with instant feedback.
- **💳 Seamless Checkout & Orders**: Smooth checkout process, order placement, order history tracking, and detailed receipts.
- **❤️ Wishlist**: Save favorite items for future shopping.
- **⚡ Admin Dashboard**: Manage inventory, add new products, update stock, and monitor orders.
- **🎨 Responsive UI/UX**: Clean, modern aesthetics styled with responsive CSS for mobile and desktop screens.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Werkzeug
- **Frontend**: HTML5, CSS3 (Modern responsive layout), JavaScript
- **Database**: SQLite (default for development), MySQL compatible
- **Testing**: Pytest / Unittest

---

## 📁 Project Structure

```
fashion store/
├── app.py                     # Main Flask application entry point & routes
├── models.py                  # Database models (User, Product, Order, Cart, etc.)
├── config.py                  # Application configuration settings
├── seed_data.py               # Database population script with initial fashion catalog
├── requirements.txt           # Python package dependencies
├── .env.example               # Template environment variables
├── .gitignore                 # Git ignore configuration
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with navbar & footer
│   ├── home.html              # Landing / hero page
│   ├── product_list.html      # Product catalog with filters
│   ├── product_detail.html    # Detailed product view
│   ├── cart.html              # Shopping cart view
│   ├── checkout.html          # Order checkout
│   ├── profile.html           # User profile & address management
│   ├── orders.html            # Order history
│   ├── wishlist.html          # Wishlist management
│   ├── login.html             # User login
│   ├── register.html          # User registration
│   ├── admin.html             # Admin management
│   └── 404.html / 500.html    # Error pages
├── static/                    # Static assets
│   ├── css/style.css          # Core design stylesheet
│   ├── js/main.js             # Clientside interactivity
│   └── images/                # Product photos & banners
└── tests/                     # Test suites
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/2004sudeeptalawar-art/fashion-store-ecommerce-web-application.git
cd fashion-store-ecommerce-web-application
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Seed the Database
```bash
python seed_data.py
```

### 6. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🧪 Running Tests

Execute the test suite using pytest:
```bash
pytest
```

---

## 👨‍💻 Author

**Sudeep Talawar**
- GitHub: [@2004sudeeptalawar-art](https://github.com/2004sudeeptalawar-art)
- Portfolio / Profile: [github.com/2004sudeeptalawar-art](https://github.com/2004sudeeptalawar-art)

---

## 📄 License

This project is licensed under the MIT License.
