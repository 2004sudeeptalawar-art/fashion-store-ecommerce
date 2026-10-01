# ⚜️ ATELIER & CO. — Haute Couture & Luxury Fashion E-Commerce

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Store-D4AF37?style=for-the-badge&logo=render&logoColor=white)](https://fashion-store-ecommerce.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL%20%7C%20MySQL-4479A1?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An editorial, high-fashion e-commerce platform crafted with a minimalist luxury design system, interactive shopping bag drawer, live product filtering, client-side QuickView, customer accounts, and an administrative operations dashboard.

---

## 🌐 Live Application
* **Production URL:** [https://fashion-store-ecommerce.onrender.com](https://fashion-store-ecommerce.onrender.com) *(Update with your deployed link)*
* **Localhost URL:** `http://127.0.0.1:5000`

---

## ✨ Features & Architecture

### 💎 Editorial Luxury Experience
* **Minimalist Couture Aesthetic:** Rich dark tones, gold accents (`#D4AF37`), subtle serif typography, and glassmorphism cards.
* **Interactive Shopping Bag:** Real-time sliding cart drawer with instant AJAX quantity updates, subtotal recalculations, and free shipping progress tracker.
* **QuickView Modal:** Preview garments, select sizes/colors, and add directly to bag without leaving the catalog.
* **Live Catalog & Filtering:** Search and filter apparel by category (Women's Runway, Men's Sartorial, Leather Goods, Jewelry & Horology), price range, and special badges (*Exclusive*, *Bestseller*, *New Arrival*).
* **Wishlist:** Save favorite designer pieces with a single click.

### 🔐 Authentication & Orders
* **Customer Accounts:** Secure registration, login session management, saved delivery addresses, and comprehensive order history with status timeline.
* **Streamlined Checkout:** Clean single-page checkout supporting multiple shipping destinations and Cash on Delivery / Card payments.
* **Order Tracking:** Detailed invoice confirmation with unique order serial (`ORD-YYYYMMDD-XXXX`).

### 👑 Admin Operations Center
* **Operations Metrics:** Live overview of total gross revenue, lifetime completed orders, catalog garment count, and registered patrons.
* **Order Pipeline Management:** Real-time order fulfillment updates (`Pending` ➔ `Confirmed` ➔ `Shipped` ➔ `Delivered` ➔ `Cancelled`).
* **Inventory Control:** Create new garments with multiple sizes and color variants or delete discontinued pieces.

---

## 🔑 Demo Access Credentials

| Role | Email | Password | Access |
|---|---|---|---|
| **Customer** | `sophia@example.com` | `user123` | Browsing, Cart, Orders, Profile |
| **Administrator** | `admin@vogue.com` | `admin123` | Admin Operations Center (`/admin`) |

---

## 🚀 Quick Start (Local Run)

### Prerequisites
* Python 3.10 or higher
* Git

### Step-by-Step

1. **Clone the repository:**
   ```bash
   git clone https://github.com/2004sudeeptalawar-art/fashion-store-ecommerce.git
   cd fashion-store-ecommerce
   ```

2. **Run using the one-click startup script (Windows):**
   ```cmd
   start.bat
   ```

3. **Or run manually via terminal:**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   # source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Start application
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your web browser. The database is pre-seeded with luxury runway products automatically on first boot!

---

## ☁️ Deployment Guide (Deploy in 3 Minutes)

This repository includes a production-ready **`Procfile`**, **`gunicorn`**, and automated database initialization for zero-configuration cloud hosting.

### Deploying to Render.com (Recommended & Free)

1. **Push your code to GitHub** (see Git Push section below).
2. Go to [Render.com](https://render.com) and sign in with GitHub.
3. Click **"New +"** &rarr; **"Web Service"**.
4. Select your repository: `fashion-store-ecommerce`.
5. Configure the deployment settings:
   * **Name:** `fashion-store-ecommerce`
   * **Environment:** `Python 3`
   * **Region:** Any close to you (e.g. Frankfurt, Oregon, Singapore)
   * **Branch:** `main`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
6. Click **"Create Web Service"**.
7. In ~2 minutes, Render will provide a live public HTTPS link (e.g., `https://fashion-store-ecommerce.onrender.com`).
8. Copy your live link and paste it into the badge above and into your GitHub repository's **About &rarr; Website** section!

---

## 📦 Project Structure

```
fashion-store/
├── app.py                # Main Flask application & routes (REST APIs, Auth, Cart, Admin)
├── config.py             # Environment configuration (SQLite, PostgreSQL, MySQL fallback)
├── models.py             # SQLAlchemy ORM models (User, Product, Variant, Cart, Order, Address)
├── seed_data.py          # Seed script with luxury apparel, variants, users & reviews
├── Procfile              # Gunicorn web process definition for cloud deployment
├── requirements.txt      # Python dependencies
├── start.bat             # One-click Windows runner script
├── push.bat              # One-click Git commit & push helper
├── static/
│   ├── css/style.css     # Luxury couture styling, glassmorphism, responsive grid
│   └── js/main.js        # Cart drawer AJAX, QuickView modal, live search, notifications
└── templates/            # Jinja2 templates (home, catalog, product, cart, checkout, admin, etc.)
```

---

## 📄 License
This project is licensed under the MIT License - open for personal and commercial portfolio use.
