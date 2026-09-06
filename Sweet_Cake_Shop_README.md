# 🍰 Sweet Cake Shop

A full-stack online cake ordering web application built with **Python, Django, SQLite, HTML, CSS and JavaScript**.

The application allows customers to browse cakes, manage a cart and wishlist, place orders, make online payments, verify payment using an **OTP sent to their email**, and track their orders. Staff/admin users can manage cakes, categories, coupons, orders, reviews, contact messages and notifications through Django Admin.

---

## ✨ Features

### 👤 Customer Features

- Browse cake catalogue
- Search cakes
- Filter cakes by category
- Eggless cake filter
- Cake detail pages with images and reviews
- Add cakes to cart
- Update/remove cart items
- Wishlist
- User registration and login
- Checkout with:
  - Customer name
  - Phone number
  - Address
  - City
  - Pincode
  - Delivery date
  - Delivery time slot
  - Cake message
  - Additional notes
- Coupon/discount support
- Cash on Delivery (COD)
- Online payment using Razorpay
- Payment verification using OTP sent to the customer's email
- My Orders page
- Order status tracking
- Custom cake request
- Ratings and reviews
- Contact Us
- About Us

---

## 💳 Payment & Order Confirmation

The project supports **Cash on Delivery** and **Razorpay online payment**.

### Online Payment Flow

```text
Add Cake
   ↓
Cart
   ↓
Checkout
   ↓
Select Razorpay
   ↓
Complete Payment
   ↓
Razorpay Payment Verification
   ↓
OTP sent to registered Email
   ↓
Enter OTP
   ↓
OTP Verified
   ↓
Payment Status = PAID
   ↓
Order Status = PLACED
   ↓
Order Confirmation Page
```

**Important:** This project does **not require a QR scanner for the normal online payment flow**. After payment verification, the OTP is sent to the customer's registered email address. The customer enters that OTP on the website to confirm the order.

### Cash on Delivery

For COD orders:

```text
Checkout
   ↓
Select COD
   ↓
Place Order
   ↓
Order Status = PLACED
```

---

## 🛠️ Technology Stack

### Backend
- Python
- Django
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Payment
- Razorpay

### Email
- Gmail SMTP
- Django Email Backend
- Payment verification OTP

### Other
- Pillow
- QRCode
- Twilio notification support

---

## 📁 Project Structure

```text
Sweet_Cake_Shop/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── db.sqlite3
│
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── notifications.py
│   ├── context_processors.py
│   └── management/
│       └── commands/
│           └── seed_data.py
│
├── sweetcake/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   └── shop/
│
├── static/
│   ├── css/
│   └── images/
│
└── media/
```

---

# 🚀 Installation & Setup

## 1. Download / Clone the Project

Open Command Prompt or PowerShell and go to the project folder:

```powershell
cd "Sweet_Cake_Shop"
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate
```

---

## 3. Install Required Packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The main dependencies include:

```text
Django
Razorpay
Pillow
qrcode
Twilio
python-dotenv
```

---

## 4. Configure Environment Variables

Create a `.env` file in the same folder as `manage.py`.

You can copy `.env.example`:

```powershell
copy .env.example .env
```

Then open `.env` and configure the values.

### Basic Configuration

```env
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Razorpay

For online payment, add your Razorpay credentials:

```env
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

Use **Razorpay Test Mode** while developing.

### Gmail SMTP for Payment OTP

The project sends the payment verification OTP to the user's registered email.

Add:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password

DEFAULT_FROM_EMAIL=yourgmail@gmail.com
```

### Gmail App Password

For Gmail SMTP, use a **Google App Password** instead of your normal Gmail password.

Do not put your real Gmail password, Razorpay secret, or other private credentials in GitHub.

---

## 5. Run Database Migrations

```powershell
python manage.py migrate
```

---

## 6. Add Sample Data

If you want the sample cakes/categories:

```powershell
python manage.py seed_data
```

---

## 7. Create Django Admin Account

Create your own admin/superuser:

```powershell
python manage.py createsuperuser
```

Enter:

```text
Username:
Email address:
Password:
Password (again):
```

The password will not be displayed while typing.

---

## 8. Start the Server

```powershell
python manage.py runserver
```

You should see something similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

---

# 🌐 Open the Website

### Customer Website

```text
http://127.0.0.1:8000/
```

### Django Admin

```text
http://127.0.0.1:8000/admin/
```

### Staff Dashboard

```text
http://127.0.0.1:8000/admin-dashboard/
```

---

# 🔐 Django Admin Panel

The Django Admin panel is used to manage the application's backend data.

From:

```text
http://127.0.0.1:8000/admin/
```

You can manage:

- Users
- Groups
- Cakes
- Categories
- Coupons
- Orders
- Order Items
- Reviews
- Contact Messages
- Custom Cake Requests
- Notifications

### Adding a Cake

Go to:

```text
Admin → Cakes → Add
```

Enter the cake name, category, price, stock, image and other details.

### Managing Orders

Go to:

```text
Admin → Orders
```

You can view:

- Order number
- Customer
- Total amount
- Order status
- Payment status
- Payment method
- Delivery date
- Order items

---

# 📦 Order Status

The application supports order tracking through different stages.

Example:

```text
PLACED
  ↓
BAKING
  ↓
OUT FOR DELIVERY
  ↓
DELIVERED
```

Staff can update the order status from the staff dashboard.

---

# 🎟️ Coupons

Coupons can be managed from:

```text
Django Admin → Coupons
```

A sample coupon may be available when using the seed data command.

---

# ⭐ Reviews

Logged-in customers can:

- Give a rating
- Write a review
- View cake reviews

Reviews can also be managed from Django Admin.

---

# 🎂 Custom Cake Requests

Customers can submit a custom cake request.

Staff can view and manage these requests from:

```text
Django Admin → Custom Cake Requests
```

---

# 📧 Payment OTP

For Razorpay online payment:

1. Customer completes the payment.
2. The server verifies the Razorpay payment information.
3. A verification OTP is generated.
4. The OTP is sent to the customer's registered email.
5. Customer enters the OTP on the OTP verification page.
6. If the OTP is correct:
   - Payment status becomes `PAID`
   - Order status becomes `PLACED`
   - Cart is cleared
   - Customer is redirected to the order confirmation page

The OTP is linked to the specific order.

---

# 🧪 Testing

For local development, use **Razorpay Test Mode**.

Do not use real payment credentials while testing.

For testing the email OTP:

1. Create a user account with a valid email address.
2. Add cakes to the cart.
3. Go to checkout.
4. Select Razorpay.
5. Complete the test payment.
6. Check the registered email inbox.
7. Copy the OTP.
8. Enter the OTP on the website.
9. Confirm that the order status changes to `PLACED`.

---

# ⚠️ Common Problems

## Problem 1: `ModuleNotFoundError`

Run:

```powershell
pip install -r requirements.txt
```

Make sure the virtual environment is activated.

---

## Problem 2: Admin says "You are authenticated but not authorized"

The account is logged in but does not have staff/admin permission.

Create a proper superuser:

```powershell
python manage.py createsuperuser
```

Or, if an existing user needs staff permission:

```powershell
python manage.py shell
```

Then:

```python
from django.contrib.auth.models import User

user = User.objects.get(username="your_username")
user.is_staff = True
user.is_superuser = True
user.save()
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

---

## Problem 3: Email OTP is not received

Check:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=yourgmail@gmail.com
```

Also check:

- The customer account has a valid email address.
- Gmail App Password is correct.
- Two-Step Verification is enabled on the Google account.
- Check the Spam/Junk folder.
- Restart the Django server after changing `.env`.

---

## Problem 4: Razorpay is not working

Check:

```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

Use Razorpay **Test Mode** credentials during development.

---

## Problem 5: Database errors after changing models

Run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

# 🔒 Security

Never upload the following to GitHub:

```text
.env
db.sqlite3
venv/
__pycache__/
*.pyc
```

The `.gitignore` file is included to help prevent sensitive/local files from being committed.

### Never expose:

- Gmail App Password
- Razorpay Secret Key
- Twilio Auth Token
- Django production `SECRET_KEY`

If a secret has already been exposed publicly, rotate/revoke it immediately.

---

# 💡 Interview Explanation

> I developed a full-stack online cake ordering application using Python and Django. The application provides a complete e-commerce flow including cake browsing, search and filtering, cart, wishlist, coupons, checkout, Cash on Delivery and Razorpay online payments. For online payments, the system verifies the payment and sends an OTP to the customer's registered email. The order is confirmed only after successful OTP verification. I also implemented order tracking, reviews, custom cake requests and a Django Admin panel for managing cakes, categories, orders, coupons, users and notifications.

---

# 📌 Future Improvements

- Deploy the application online
- Add a production database such as PostgreSQL
- Add cloud image storage
- Add automated email order confirmations
- Add payment webhooks
- Improve admin analytics
- Add product recommendations
- Add automated testing

---

## 👨‍💻 Project

**Sweet Cake Shop**  
Built with **Python + Django**

