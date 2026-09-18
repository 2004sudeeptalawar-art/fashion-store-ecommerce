# Fashion Store Project

## Overview
The Fashion Store project is a web application built using Flask that allows users to browse and purchase fashion products. It features user authentication, a shopping cart, and order management functionalities.

## Project Structure
```
fashion-store
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── models
│   │   ├── product.py
│   │   ├── user.py
│   │   └── order.py
│   ├── routes
│   │   ├── auth.py
│   │   ├── cart.py
│   │   ├── products.py
│   │   └── orders.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── products.html
│   │   ├── cart.html
│   │   └── checkout.html
│   └── static
│       ├── css
│       │   └── style.css
│       └── js
│           └── main.js
├── migrations
├── tests
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd fashion-store
   ```

2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Ensure you have a MySQL database named `fashion_store`.
   - Update the database credentials in `app/config.py`:
     ```python
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/fashion_store'
     ```

5. **Run Migrations**
   ```
   flask db upgrade
   ```

6. **Run the Application**
   ```
   python run.py
   ```

## Usage
- Navigate to `http://localhost:5000` in your web browser to access the application.
- Users can register, log in, browse products, add items to their cart, and place orders.

## Testing
- Unit tests are located in the `tests` directory. Run tests using:
  ```
  pytest
  ```

## License
This project is licensed under the MIT License.