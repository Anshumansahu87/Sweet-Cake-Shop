# 🍰 Sweet Cake Shop — Python + Django Internship Project

A complete beginner-friendly Django e-commerce application for an online cake shop.

## Main features

### Customer
- Cake catalogue with images, search, category and eggless filter
- Cake details
- Session-based cart and wishlist
- Signup / login / logout
- Checkout with delivery date, time slot, cake message and notes
- Coupon system (`SWEET10` in demo data)
- COD
- Razorpay Test/Live integration with server-side signature verification
- Optional UPI QR fallback
- Custom cake request form
- Reviews and ratings
- My Orders with order tracking timeline
- About Us / Contact Us
- Animated cart emojis and interactive UI

### Admin / Staff
- Custom `/admin-dashboard/`
- Sales and order overview
- Low stock list
- Recent orders
- Update order status from dashboard
- Customer notification log
- Custom cake requests
- Full Django `/admin/` for cakes, categories, coupons, orders, reviews, contact messages, users and notifications

### Customer notifications
The project has a notification service. Without external credentials it records a `DEMO` notification so local development works. With Twilio credentials it can send real SMS; WhatsApp can also be configured.

## Payment note
Razorpay integration is real integration code, but Live payments require your own Razorpay account, KYC/activation and Live API keys. Test keys are recommended while developing. Never put the secret key in frontend code or GitHub.

## Quick start (Windows PowerShell)

```powershell
cd "C:\Users\LENOVO\Downloads\Sweet_Cake_Shop_COMPLETE"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Custom Dashboard: http://127.0.0.1:8000/admin-dashboard/
- Django Admin: http://127.0.0.1:8000/admin/

## If Python 3.14 gives venv/pip problems
Use the normal Python Launcher and try:
```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
The application code is standard Django and does not depend on a separate database server.

## Real SMS
Copy `.env.example` to `.env`, fill Twilio credentials, and use a phone number allowed by your Twilio account. The project stores every notification attempt in the `Notification` table.

## Important: `.env` is loaded automatically
After copying `.env.example` to `.env`, Django loads the values automatically. Do not paste your Razorpay secret into HTML, JavaScript, GitHub, or chat.

## Real payments
Copy `.env.example` to `.env` and add Razorpay credentials. Start with Test Mode. After your Razorpay account is approved for Live Mode, replace the keys with Live keys and deploy behind HTTPS. Payment success is accepted only after server-side signature verification.

## Interview explanation
> I built a full-stack online cake ordering application using Python and Django. Django Models manage cakes, categories, orders, order items, reviews, coupons, custom cake requests and notifications. Django Forms validate registration and checkout input. Views handle the business logic, while templates provide the customer UI and custom staff dashboard. The application supports cart, wishlist, coupons, COD, Razorpay payment verification, order tracking and customer notifications.

## Demo QR payment (recommended for internship presentation)

This project includes a local demo payment flow that does not charge real money. On the payment page, the customer can scan the QR code and open the demo confirmation page, then confirm the payment. Django marks the order as `PAID`, creates the customer notification, clears the cart, and shows the order confirmation message.

For phone-to-PC QR testing, run Django on the local network:

```powershell
python manage.py runserver 0.0.0.0:8000
```

Then put your computer's LAN address in `.env`, for example `DEMO_QR_HOST=192.168.1.5:8000`. The phone and computer must be on the same Wi-Fi network.


## Phone QR demo

1. Keep laptop and phone on the same Wi-Fi.
2. Set `DEMO_QR_HOST=192.168.1.113:8000` in `.env` (replace with your laptop IPv4 if it changes).
3. Install QR support inside the active virtual environment: `python -m pip install "qrcode[pil]"`.
4. Run: `python manage.py runserver 0.0.0.0:8000`.
5. On the laptop use `http://127.0.0.1:8000/`; scan the payment QR with the phone Camera/Google Lens.
6. The QR opens a signed, phone-friendly order confirmation page without requiring customer login.
7. Confirming the demo order marks it PAID/PLACED and creates the customer notification record. No real money is charged.

If the laptop IP changes, update `DEMO_QR_HOST` and restart Django.


## Phone QR testing

For a phone on the same Wi-Fi as the laptop, keep `DEMO_QR_HOST=192.168.1.113:8000` and run:

```powershell
python manage.py runserver 0.0.0.0:8000
```

For a phone on another network (or for "anyone" to scan), a private `192.168.x.x` address cannot be used. Start a public HTTPS tunnel to port 8000 (for example with ngrok), then set `DEMO_QR_HOST` to the complete HTTPS URL shown by the tunnel. Restart Django and generate a new QR for the order. The QR will then open the signed phone confirmation page.

The demo confirmation does not charge real money. Real SMS requires configured Twilio credentials.
