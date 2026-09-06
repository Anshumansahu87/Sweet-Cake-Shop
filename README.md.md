# 🍰 Sweet Cake Shop

A complete **online cake ordering web application** built with **Django**. Customers can browse cakes, search/filter products, manage a cart and wishlist, request custom cakes, apply coupons, place orders, pay online using Razorpay, and verify online payments using an email OTP.

---

## 📌 Project Overview

Sweet Cake Shop provides an end-to-end online ordering experience:

```text
Customer
   ↓
Browse Cakes
   ↓
Select Cake
   ↓
Add to Cart
   ↓
Checkout
   ↓
Choose Payment Method
   ├── Cash on Delivery → Order Confirmed
   │
   └── Razorpay
          ↓
      Payment Verified
          ↓
      Email OTP Sent
          ↓
      Enter OTP
          ↓
      OTP Verified
          ↓
      Order Confirmed
          ↓
      Order Success Page
```

---

# ✨ Features

## 👤 Customer Features

- User registration and login
- Browse available cakes
- Search cakes by name
- Filter cakes by category
- Filter eggless cakes
- View cake details
- Add cakes to cart
- Update cart quantity
- Remove items from cart
- Wishlist
- Custom cake request
- Coupon/discount support
- Cake reviews and ratings
- Checkout and delivery details
- Order history
- Cash on Delivery
- Razorpay online payment
- Email OTP verification for online payment
- Order confirmation email

## 🛠️ Admin Features

- Django Admin panel
- Manage categories
- Manage cakes
- Manage coupons
- Manage custom cake requests
- Manage orders and order items
- Manage reviews
- Manage customer contact messages
- Admin dashboard
- View sales/order statistics
- Update order status
- Monitor cake stock

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Frontend interaction |
| Bootstrap | Responsive UI |
| Razorpay | Online payment |
| Gmail SMTP | Email and OTP |
| Pillow | Image processing |
| python-dotenv | Environment variables |

---

# 📁 Project Structure

```text
Sweet_Cake_Shop/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── sweetcake/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_order_otp_order_otp_verified.py
│   │
│   ├── templates/
│   │   └── shop/
│   │       ├── home.html
│   │       ├── cakes.html
│   │       ├── detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── payment.html
│   │       ├── otp_verify.html
│   │       ├── success.html
│   │       ├── orders.html
│   │       ├── signup.html
│   │       ├── login.html
│   │       ├── wishlist.html
│   │       ├── custom_cake.html
│   │       ├── contact.html
│   │       ├── about.html
│   │       └── admin_dashboard.html
│   │
│   └── static/
│       └── shop/
│           ├── css/
│           ├── js/
│           └── images/
│
└── media/
    └── cakes/
```

> Folder names can differ slightly depending on your local project structure. The important parts are the Django project, `shop` app, templates, static files, migrations, `manage.py`, and configuration files.

---

# 🚀 How to Run the Project

Follow these steps in order.

## Step 1 — Install Python

Make sure Python is installed.

Check:

```bash
python --version
```

If `python` does not work on Windows, try:

```bash
py --version
```

---

## Step 2 — Open the Project in VS Code

Open the `Sweet_Cake_Shop` folder in VS Code.

Open the VS Code terminal:

```text
Terminal → New Terminal
```

---

## Step 3 — Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

If activation works, the terminal normally shows:

```text
(venv)
```

before the current path.

---

## Step 4 — Install Required Packages

Run:

```bash
pip install -r requirements.txt
```

The project uses the packages listed in `requirements.txt`.

---

# 🔐 Step 5 — Configure Environment Variables

Create a file named:

```text
.env
```

in the same folder as `manage.py`.

Example:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

### Important

Never upload `.env` to GitHub.

Your `.env` contains private credentials such as:

- Django Secret Key
- Gmail App Password
- Razorpay Secret Key

Use `.env.example` as the template for other developers.

---

# 📧 Step 6 — Configure Gmail OTP

The project sends the online payment OTP through email.

For Gmail SMTP:

1. Open your Google Account.
2. Enable **2-Step Verification**.
3. Create a **Google App Password**.
4. Put the generated App Password in:

```env
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

Do **not** use your normal Gmail password.

The OTP flow is:

```text
Razorpay Payment
      ↓
Payment Signature Verified
      ↓
6-Digit OTP Generated
      ↓
OTP Sent to Customer Email
      ↓
Customer Enters OTP
      ↓
OTP Verified
      ↓
Payment Status = PAID
      ↓
Order Status = PLACED
```

---

# 💳 Step 7 — Configure Razorpay

Add your Razorpay credentials to `.env`:

```env
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

For development/testing, use the appropriate Razorpay test credentials.

Never upload your Razorpay secret key to GitHub.

---

# 🗄️ Step 8 — Setup Database

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

This creates/updates the database tables.

If migrations are already present, normally:

```bash
python manage.py migrate
```

is enough.

---

# 👨‍💼 Step 9 — Create Admin Account

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username
Email
Password
```

Then the admin panel can be opened at:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔍 Step 10 — Check Django Project

Before starting the server:

```bash
python manage.py check
```

Expected result:

```text
System check identified no issues
```

---

# ▶️ Step 11 — Start the Development Server

Run:

```bash
python manage.py runserver
```

Open the website:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

To stop the server:

```text
CTRL + C
```

---

# 🛒 Customer Order Flow

## Cash on Delivery

```text
Login
 ↓
Select Cake
 ↓
Add to Cart
 ↓
Checkout
 ↓
Select COD
 ↓
Place Order
 ↓
Order Confirmed
 ↓
Confirmation Email
```

## Online Payment

```text
Login
 ↓
Select Cake
 ↓
Add to Cart
 ↓
Checkout
 ↓
Select Razorpay
 ↓
Create Razorpay Payment
 ↓
Complete Payment
 ↓
Razorpay Signature Verification
 ↓
OTP Sent to Email
 ↓
Enter OTP
 ↓
OTP Verified
 ↓
Order Confirmed
 ↓
Confirmation Page
```

---

# 📦 Order Status

The admin can manage the order status from the admin dashboard.

Typical flow:

```text
PLACED
  ↓
BAKING
  ↓
OUT_FOR_DELIVERY
  ↓
DELIVERED
```

---

# 🧁 Admin Workflow

After logging into:

```text
http://127.0.0.1:8000/admin/
```

the admin can manage:

```text
Categories
Cakes
Coupons
Custom Cake Requests
Orders
Order Items
Reviews
Contact Messages
```

The custom admin dashboard also provides information about orders, sales, customers, cakes, stock, and pending orders.

---

# 🧪 Troubleshooting

## Error: `No module named django`

Run:

```bash
pip install -r requirements.txt
```

Make sure the virtual environment is activated.

---

## Error: `python is not recognized`

Try:

```bash
py manage.py runserver
```

or reinstall Python with **Add Python to PATH** enabled.

---

## Gmail OTP is not being received

Check:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

Also check the Gmail spam folder.

---

## Razorpay payment is not working

Check:

```env
RAZORPAY_KEY_ID=...
RAZORPAY_KEY_SECRET=...
```

Also make sure the Razorpay package is installed:

```bash
pip install razorpay
```

---

## Database error

Run:

```bash
python manage.py migrate
```

Then:

```bash
python manage.py check
```

---

# 🔒 GitHub Security

Before pushing the project to GitHub, make sure these are ignored:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

Do not upload:

```text
.env
Gmail App Password
Razorpay Secret Key
Django Secret Key
```

---

# 📤 Push Changes to GitHub

If the repository is already connected:

```bash
git add .
git commit -m "Update Sweet Cake Shop"
git push
```

If the repository is not connected yet:

```bash
git remote add origin https://github.com/Anshumansahu87/Sweet_Cake_Shop.git
git branch -M main
git push -u origin main
```

After that, future changes only need:

```bash
git add .
git commit -m "Update project"
git push
```

---

# 🌐 Local vs Live Server

`python manage.py runserver` is for **local development**.

It opens:

```text
http://127.0.0.1:8000/
```

This address is normally accessible only from your computer.

For a public website, the Django project must be deployed to a hosting service and production settings must be configured.

---

# 👨‍💻 Author

**Anshuman Sahu**

GitHub: https://github.com/Anshumansahu87

LinkedIn: https://www.linkedin.com/in/anshuman87/

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
