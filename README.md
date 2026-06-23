# SKSphere

SKSphere is a modern Django-based E-Commerce platform designed to provide a seamless online shopping experience. The platform includes user authentication, product management, cart functionality, wishlist management, order tracking, product reviews, and secure password recovery using OTP verification.

---

## Features

### User Management

* User Registration
* User Login & Logout
* User Profile Management
* Edit Profile
* Change Password
* Forgot Password with OTP Verification

### Product Management

* Product Categories
* Featured Products
* Trending Products
* Best Seller Products
* Product Details Page
* Product Search

### Shopping Features

* Shopping Cart
* Wishlist
* Add to Cart
* Update Cart Quantity
* Remove Cart Items

### Order Management

* Place Orders
* Order Tracking
* Order History
* Order Status Updates

### Reviews & Ratings

* Product Reviews
* Product Ratings
* One Review Per User

### Security Features

* Password Hashing
* CSRF Protection
* Session Authentication
* OTP-Based Password Recovery

---

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Database

* SQLite3

### Email Service

* Gmail SMTP

---

## Project Structure

```text
SKSphere/
│
├── accounts/
├── cart/
├── orders/
├── products/
├── static/
├── media/
├── SKSphere/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation Guide

### Clone Repository

```bash
git clone https://github.com/shivakumar-karnati/SKSphere.git
cd SKSphere
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_app_password
```

### Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Future Improvements

* Online Payment Gateway Integration
* Product Recommendation System
* Email Notifications
* Admin Analytics Dashboard
* Coupon System
* Multiple Product Images
* Product Variants
* Deployment on Render

---

## Author

Shiva Kumar Karnati

GitHub:
https://github.com/shivakumar-karnati

---

## License

This project is created for educational and portfolio purposes.
