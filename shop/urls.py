from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("cakes/", views.cake_list, name="cakes"),
    path("cake/<slug:slug>/", views.cake_detail, name="detail"),
    path("cake/<int:cake_id>/review/", views.add_review, name="add_review"),

    path("wishlist/", views.wishlist_page, name="wishlist"),
    path("wishlist/toggle/<int:cake_id>/", views.toggle_wishlist, name="toggle_wishlist"),

    path("cart/", views.cart_page, name="cart"),
    path("cart/add/<int:cake_id>/", views.add_to_cart, name="add_cart"),
    path("cart/update/<int:cake_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:cake_id>/", views.remove_from_cart, name="remove_cart"),

    path("custom-cake/", views.custom_cake, name="custom_cake"),

    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="shop/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("checkout/", views.checkout, name="checkout"),
    path("payment/<str:order_number>/", views.payment, name="payment"),
    path("payment/<str:order_number>/create/", views.create_payment, name="create_payment"),
    path("payment/<str:order_number>/qr/", views.payment_qr, name="payment_qr"),
    path("phone-pay/<str:token>/", views.phone_demo_confirm, name="phone_demo_confirm"),
    path("payment/<str:order_number>/demo-confirm/", views.demo_confirm_payment, name="demo_confirm_payment"),
   
    path(
    "payment/<str:order_number>/verify/",
    views.verify_payment,
    name="verify_payment"
),

path(
    "payment/<str:order_number>/otp/",
    views.verify_payment_otp,
    name="verify_payment_otp"
),

    path("order-success/<str:order_number>/", views.order_success, name="order_success"),
    path("orders/", views.my_orders, name="orders"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/order/<str:order_number>/status/", views.update_order_status, name="update_order_status"),
]
