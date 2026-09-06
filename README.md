# 🍰 Sweet Cake Shop

A Django-based online cake ordering website where customers can browse cakes, add items to a cart, place orders, make online payments using Razorpay, and verify online payments through an email OTP.

## ✨ Features

- 🧁 Browse cakes by category
- 🔎 Search cakes
- 🥚 Eggless cake filter
- 🛒 Add, update, and remove cart items
- ❤️ Wishlist
- 🎂 Custom cake request
- 🎟️ Coupon/discount support
- ⭐ Cake reviews and ratings
- 👤 User signup/login
- 📦 Customer order history
- 💳 Razorpay online payment
- 🔐 Email OTP verification after successful Razorpay payment
- 💵 Cash on Delivery (COD)
- 📧 Order confirmation email
- 🛠️ Django Admin panel
- 📊 Admin dashboard for orders, sales, cakes, customers, and stock
- 📩 Contact form

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Razorpay
- Gmail SMTP
- Pillow
- python-dotenv

## 📁 Project Structure

```text
Sweet_Cake_Shop/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── Sweet_Cake_Shop/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── shop/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── templates/
│   │   └── shop/
│   └── static/
│       └── shop/
│
└── media/
    └── cakes/
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Anshumansahu87/Sweet_Cake_Shop.git
cd Sweet_Cake_Shop
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the same folder as `manage.py`.

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

### ⚠️ Gmail App Password

For Gmail SMTP, use a **Google App Password**, not your normal Gmail password.

Keep your `.env` file private and never upload it to GitHub.

## 🗄️ Database Setup

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin account:

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to create the username, email, and password.

## ▶️ Run the Project

Start Django's development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## 💳 Payment Flow

For online payment, the project uses Razorpay.

The flow is:

```text
Checkout
   ↓
Create Order
   ↓
Razorpay Payment
   ↓
Razorpay Payment Verification
   ↓
6-Digit OTP Sent to Customer Email
   ↓
Customer Enters OTP
   ↓
OTP Verified
   ↓
Order Confirmed
   ↓
Order Success Page
```

The project also supports Cash on Delivery.

## 📧 Email

The application uses Gmail SMTP for:

- Payment verification OTP
- Order confirmation email

Make sure the Gmail account has SMTP/App Password configured correctly.

## 🔐 Security

Do not upload these files or values to GitHub:

- `.env`
- Gmail App Password
- Razorpay Secret Key
- Django Secret Key
- Any other private credentials

The `.gitignore` file should include:

```gitignore
.env
venv/
__pycache__/
db.sqlite3
```

## 🧪 Check the Project

Before running or deploying:

```bash
python manage.py check
```

If everything is correct, Django should report:

```text
System check identified no issues
```

## 🚀 GitHub Update

After making changes:

```bash
git add .
git commit -m "Update project"
git push
```

Only changed files are updated in the existing GitHub repository.

## 👨‍💻 Author

**Anshuman Sahu**

GitHub: https://github.com/Anshumansahu87

LinkedIn: https://www.linkedin.com/in/anshuman87/
