from django.core import signing
from django.core.mail import send_mail
import random
from twilio.rest import Client
import json
import uuid
import socket
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.db import transaction
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core import signing

from .forms import CheckoutForm, SignupForm, CustomCakeForm
from .models import (
    Cake, Category, Coupon, Order, OrderItem, Review, ContactMessage,
)
from .notifications import send_customer_notification

try:
    import razorpay
except ImportError:
    razorpay = None


def home(request):
    return render(request, "shop/home.html", {
        "categories": Category.objects.all(),
        "featured": Cake.objects.filter(featured=True, stock__gt=0)[:8],
    })


def cake_list(request):
    cakes = Cake.objects.filter(stock__gt=0).select_related("category")
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    eggless = request.GET.get("eggless", "").strip()

    if q:
        cakes = cakes.filter(name__icontains=q)
    if category:
        cakes = cakes.filter(category__slug=category)
    if eggless == "1":
        cakes = cakes.filter(eggless=True)

    return render(request, "shop/cakes.html", {
        "cakes": cakes,
        "categories": Category.objects.all(),
        "q": q,
        "selected_category": category,
        "eggless": eggless,
    })


def cake_detail(request, slug):
    cake = get_object_or_404(
        Cake.objects.prefetch_related("reviews__user"), slug=slug
    )
    return render(request, "shop/detail.html", {
        "cake": cake,
        "reviews": cake.reviews.all(),
    })


def add_to_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    if cake.stock <= 0:
        messages.error(request, "This cake is out of stock.")
        return redirect("shop:cakes")

    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        quantity = 1

    cart = request.session.get("cart", {})
    current = int(cart.get(str(cake.id), 0))
    cart[str(cake.id)] = min(current + quantity, cake.stock)
    request.session["cart"] = cart
    messages.success(request, f"{cake.name} added to your cart.")
    return redirect("shop:cart")


def update_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(cake_id), None)
    else:
        cart[str(cake_id)] = min(quantity, cake.stock)
    request.session["cart"] = cart
    return redirect("shop:cart")


def remove_from_cart(request, cake_id):
    cart = request.session.get("cart", {})
    cart.pop(str(cake_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "Cake removed from your cart.")
    return redirect("shop:cart")


def cart_page(request):
    cart = request.session.get("cart", {})
    ids = [int(x) for x in cart.keys()]
    cakes = {str(c.id): c for c in Cake.objects.filter(id__in=ids)}
    items, total = [], Decimal("0.00")
    for cake_id, quantity in cart.items():
        cake = cakes.get(str(cake_id))
        if cake:
            quantity = min(int(quantity), cake.stock)
            subtotal = cake.price * quantity
            total += subtotal
            items.append({"cake": cake, "quantity": quantity, "subtotal": subtotal})
    return render(request, "shop/cart.html", {"items": items, "total": total})


@staff_member_required(login_url="/admin/login/")
def admin_dashboard(request):
    from django.contrib.auth.models import User
    orders = Order.objects.select_related("user").prefetch_related("items__cake")
    paid_orders = orders.filter(payment_status__in=["PAID", "COD"])
    context = {
        "total_orders": orders.count(),
        "total_sales": paid_orders.aggregate(s=Sum("total"))["s"] or 0,
        "total_cakes": Cake.objects.count(),
        "customers": User.objects.filter(is_staff=False).count(),
        "pending_orders": orders.filter(status__in=["PLACED", "BAKING"]).count(),
        "delivered_orders": orders.filter(status="DELIVERED").count(),
        "paid_online": orders.filter(payment_status="PAID").count(),
        "recent_orders": orders[:8],
        "low_stock": Cake.objects.filter(stock__lte=5).order_by("stock")[:6],
        "custom_requests": __import__("shop.models", fromlist=["CustomCakeRequest"]).CustomCakeRequest.objects.select_related("user")[:6],
        "notifications": __import__("shop.models", fromlist=["Notification"]).Notification.objects.select_related("user").order_by("-created_at")[:6],
    }
    return render(request, "shop/admin_dashboard.html", context)


def wishlist_page(request):
    wishlist = [str(x) for x in request.session.get("wishlist", [])]
    cakes = Cake.objects.filter(id__in=wishlist, stock__gt=0).select_related("category")
    return render(request, "shop/wishlist.html", {"cakes": cakes})


def toggle_wishlist(request, cake_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    cake = get_object_or_404(Cake, id=cake_id)
    wishlist = [str(x) for x in request.session.get("wishlist", [])]
    key = str(cake.id)
    if key in wishlist:
        wishlist.remove(key)
        saved = False
        message = f"{cake.name} removed from your wishlist."
    else:
        wishlist.append(key)
        saved = True
        message = f"{cake.name} added to your wishlist. ❤️"
    request.session["wishlist"] = wishlist
    request.session.modified = True
    return JsonResponse({"saved": saved, "count": len(wishlist), "message": message})


def signup(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("shop:home")
    return render(request, "shop/signup.html", {"form": form})


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("shop:cakes")

    ids = [int(x) for x in cart.keys()]
    cakes = {str(c.id): c for c in Cake.objects.filter(id__in=ids)}
    items, subtotal = [], Decimal("0.00")

    for cake_id, quantity in cart.items():
        cake = cakes.get(str(cake_id))
        if not cake or cake.stock < int(quantity):
            messages.error(request, "One or more cakes do not have enough stock.")
            return redirect("shop:cart")
        quantity = int(quantity)
        subtotal += cake.price * quantity
        items.append((cake, quantity))

    discount = Decimal("0.00")
    coupon_code = ""
    form = CheckoutForm(request.POST or None, initial={
        "customer_name": request.user.get_full_name(),
        "payment_method": "COD",
        "delivery_date": __import__("django.utils.timezone", fromlist=["localdate"]).localdate(),
    })

    if request.method == "POST" and form.is_valid():
        coupon_code = form.cleaned_data["coupon_code"].strip().upper()
        coupon = Coupon.objects.filter(code=coupon_code, active=True).first() if coupon_code else None
        if coupon:
            if subtotal < coupon.min_order:
                form.add_error("coupon_code", f"Minimum order for this coupon is ₹{coupon.min_order}.")
            else:
                discount = (subtotal * Decimal(coupon.discount_percent) / Decimal("100")).quantize(Decimal("0.01"))
        elif coupon_code:
            form.add_error("coupon_code", "Invalid or inactive coupon code.")

        if not form.errors:
            total = max(Decimal("0.00"), subtotal - discount)
            order = Order.objects.create(
                user=request.user,
                order_number="SC" + uuid.uuid4().hex[:10].upper(),
                customer_name=form.cleaned_data["customer_name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                pincode=form.cleaned_data["pincode"],
                delivery_date=form.cleaned_data["delivery_date"],
                delivery_slot=form.cleaned_data["delivery_slot"],
                custom_message=form.cleaned_data["custom_message"],
                notes=form.cleaned_data["notes"],
                subtotal=subtotal,
                discount=discount,
                total=total,
                coupon_code=coupon_code,
                payment_method=form.cleaned_data["payment_method"],
            )
            for cake, quantity in items:
                OrderItem.objects.create(order=order, cake=cake, quantity=quantity, price=cake.price)

            if order.payment_method == "COD":
                _confirm_order(order, items, payment_status="COD")
                request.session["cart"] = {}
                _notify_order(order, "placed")
                return redirect("shop:order_success", order_number=order.order_number)

            return redirect("shop:payment", order_number=order.order_number)

    total_preview = max(Decimal("0.00"), subtotal - discount)
    return render(request, "shop/checkout.html", {
        "form": form, "total": total_preview, "subtotal": subtotal, "discount": discount
    })


def _confirm_order(order, items, payment_status):
    with transaction.atomic():
        order.payment_status = payment_status
        order.status = "PLACED"
        order.save(update_fields=["payment_status", "status"])
        for cake, quantity in items:
            cake.stock -= quantity
            cake.save(update_fields=["stock"])


def _notify_order(order, event):
    if event == "placed":
        text = (
            "Sweet Cake Shop: Your order has been successfully placed. "
            "Thank you for ordering!"
        )
    elif event == "baking":
        text = f"Sweet Cake Shop: Order {order.order_number} is now being baked. 🎂"
    elif event == "out":
        text = f"Sweet Cake Shop: Order {order.order_number} is out for delivery. 🚚"
    elif event == "delivered":
        text = f"Sweet Cake Shop: Order {order.order_number} has been delivered. Enjoy your cake! 🎉"
    else:
        text = f"Sweet Cake Shop: Order {order.order_number} status updated."

    send_customer_notification(
        user=order.user,
        phone=order.phone,
        message=text,
        order=order,
        channel="SMS",
    )


@login_required
def payment(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related("items__cake"), order_number=order_number, user=request.user)
    configured = bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET and razorpay)
    demo_enabled = bool(getattr(settings, "DEMO_PAYMENT", True))
    return render(request, "shop/payment.html", {
        "order": order,
        "configured": configured,
        "demo_enabled": demo_enabled,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "upi_id": settings.UPI_ID,
    })


def _qr_signer():
    return signing.TimestampSigner(salt="sweet-cake-shop-phone-qr")


def _qr_token(order_number):
    return _qr_signer().sign(order_number)


def _order_from_qr_token(token):
    try:
        order_number = _qr_signer().unsign(token, max_age=24 * 60 * 60)
    except signing.BadSignature:
        return None
    return Order.objects.prefetch_related("items__cake", "notifications").filter(order_number=order_number).first()


def _phone_payment_url(request, order):
    # For phone scanning, DEMO_QR_HOST may be either:
    #   192.168.1.113:8000              (same Wi-Fi)
    #   https://your-public-tunnel.example (internet/public tunnel)
    configured = getattr(settings, "DEMO_QR_HOST", "").strip()
    if configured.startswith(("http://", "https://")):
        base = configured.rstrip("/")
    else:
        host = configured or request.get_host()
        scheme = "https" if request.is_secure() else "http"
        base = f"{scheme}://{host}"
    token = _qr_token(order.order_number)
    return f"{base}{reverse('shop:phone_demo_confirm', args=[token])}"


def payment_qr(request, order_number):
    """Public QR image: scanning it on a phone opens this order's signed demo page."""
    if not getattr(settings, "DEMO_PAYMENT", True):
        return JsonResponse({"error": "Demo payment mode is disabled."}, status=404)
    order = get_object_or_404(Order, order_number=order_number)
    try:
        import qrcode
        from io import BytesIO
        payload = _phone_payment_url(request, order)
        image = qrcode.make(payload)
        buf = BytesIO()
        image.save(buf, format="PNG")
        response = HttpResponse(buf.getvalue(), content_type="image/png")
        response["Cache-Control"] = "no-store"
        return response
    except ImportError:
        return JsonResponse({"error": "QR dependency missing. Run: python -m pip install \"qrcode[pil]\""}, status=500)


def phone_demo_confirm(request, token):
    """Phone-friendly signed order page. No customer login is required."""
    if not getattr(settings, "DEMO_PAYMENT", True):
        return render(request, "shop/phone_confirm.html", {"invalid": True, "message": "Demo payment mode is disabled."}, status=404)
    order = _order_from_qr_token(token)
    if not order:
        return render(request, "shop/phone_confirm.html", {"invalid": True, "message": "This QR link is invalid or has expired."}, status=404)

    if request.method == "POST":
        if order.payment_status != "PAID":
            with transaction.atomic():
                order.payment_status = "PAID"
                order.payment_method = "DEMO_UPI"
                order.status = "PLACED"
                order.razorpay_payment_id = "DEMO-" + uuid.uuid4().hex[:12].upper()
                order.save(update_fields=["payment_status", "payment_method", "status", "razorpay_payment_id"])
                for item in order.items.select_related("cake"):
                    if item.cake.stock < item.quantity:
                        return render(request, "shop/phone_confirm.html", {
                            "order": order, "invalid": True,
                            "message": f"Not enough stock for {item.cake.name}."
                        }, status=409)
                    item.cake.stock -= item.quantity
                    item.cake.save(update_fields=["stock"])
            _notify_order(order, "placed")
        return render(request, "shop/phone_confirm.html", {
            "order": order, "confirmed": True,
            "notification": order.notifications.order_by("-created_at").first(),
        })

    return render(request, "shop/phone_confirm.html", {"order": order, "token": token})


@login_required
def demo_confirm_payment(request, order_number):
    """Keep the original laptop demo button working."""
    if not getattr(settings, "DEMO_PAYMENT", True):
        messages.error(request, "Demo payment mode is disabled.")
        return redirect("shop:payment", order_number=order_number)
    order = get_object_or_404(Order.objects.prefetch_related("items__cake"), order_number=order_number, user=request.user)
    if order.payment_status != "PAID":
        with transaction.atomic():
            order.payment_status = "PAID"
            order.payment_method = "DEMO_UPI"
            order.status = "PLACED"
            order.razorpay_payment_id = "DEMO-" + uuid.uuid4().hex[:12].upper()
            order.save(update_fields=["payment_status", "payment_method", "status", "razorpay_payment_id"])
            for item in order.items.select_related("cake"):
                if item.cake.stock < item.quantity:
                    messages.error(request, f"Not enough stock for {item.cake.name}.")
                    return redirect("shop:cart")
                item.cake.stock -= item.quantity
                item.cake.save(update_fields=["stock"])
        request.session["cart"] = {}
        _notify_order(order, "placed")
    request.session["demo_payment_success"] = True
    return redirect("shop:order_success", order_number=order.order_number)


@login_required
def create_payment(request, order_number):
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST required",
            },
            status=405,
        )

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user,
    )

    # Already paid
    if order.payment_status == "PAID":
        return JsonResponse({
            "success": True,
            "already_paid": True,
            "url": reverse(
                "shop:order_success",
                args=[order.order_number],
            ),
        })

    # Check Razorpay configuration
    if not (
        settings.RAZORPAY_KEY_ID
        and settings.RAZORPAY_KEY_SECRET
        and razorpay
    ):
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Razorpay is not configured. "
                    "Check RAZORPAY_KEY_ID and "
                    "RAZORPAY_KEY_SECRET in .env."
                ),
            },
            status=400,
        )

    try:
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        razor_order = client.order.create({
            "amount": int(order.total * 100),
            "currency": "INR",
            "receipt": order.order_number,
        })

        order.razorpay_order_id = razor_order["id"]

        order.save(
            update_fields=[
                "razorpay_order_id",
            ]
        )

        return JsonResponse({
            "success": True,
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": razor_order["id"],
            "amount": int(order.total * 100),
            "currency": "INR",
            "name": "Sweet Cake Shop",
            "description": (
                f"Cake order {order.order_number}"
            ),
        })

    except Exception as exc:
        print(
            "RAZORPAY CREATE ORDER ERROR:",
            exc,
        )

        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )


@login_required
def verify_payment(request, order_number):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST required"
            },
            status=405
        )

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    # Already paid
    if order.payment_status == "PAID":
        return JsonResponse({
            "success": True,
            "url": reverse(
                "shop:order_success",
                args=[order.order_number]
            )
        })

    # Razorpay configuration
    if not (
        settings.RAZORPAY_KEY_ID
        and settings.RAZORPAY_KEY_SECRET
        and razorpay
    ):
        return JsonResponse({
            "success": False,
            "error": "Razorpay is not configured."
        }, status=400)

    try:
        data = json.loads(request.body)

        razorpay_order_id = data.get(
            "razorpay_order_id"
        )

        razorpay_payment_id = data.get(
            "razorpay_payment_id"
        )

        razorpay_signature = data.get(
            "razorpay_signature"
        )

        if not razorpay_order_id:
            raise ValueError(
                "Razorpay order ID is missing."
            )

        if not razorpay_payment_id:
            raise ValueError(
                "Razorpay payment ID is missing."
            )

        if not razorpay_signature:
            raise ValueError(
                "Razorpay signature is missing."
            )

        # Make sure payment belongs to this order
        if razorpay_order_id != order.razorpay_order_id:
            raise ValueError(
                "Payment order mismatch."
            )

        # Razorpay client
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id":
                razorpay_order_id,

            "razorpay_payment_id":
                razorpay_payment_id,

            "razorpay_signature":
                razorpay_signature,
        })

        # Generate 6 digit OTP
        otp = str(
            random.randint(100000, 999999)
        )

        # Save Razorpay details + OTP
        order.razorpay_payment_id = (
            razorpay_payment_id
        )

        order.razorpay_signature = (
            razorpay_signature
        )

        order.otp = otp
        order.otp_verified = False

        # Keep the order pending until the customer proves the OTP.
        order.payment_status = "PENDING"
        order.payment_method = "RAZORPAY"

        order.save(
            update_fields=[
                "razorpay_payment_id",
                "razorpay_signature",
                "otp",
                "otp_verified",
                "payment_status",
                "payment_method",
            ]
        )

        # Remember which order is waiting for OTP.
        request.session["payment_otp_order"] = order.order_number

               # ==============================
        # SEND OTP BY EMAIL
        # ==============================

        email = (request.user.email or "").strip()

        if not email:
            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "No email address is associated with your account. "
                        "Please add your email address first."
                    ),
                },
                status=400,
            )

        try:
            send_mail(
                subject="Sweet Cake Shop - Payment OTP",
                message=(
                    f"Hello {request.user.get_full_name() or request.user.username},\n\n"
                    f"Your payment verification OTP is: {otp}\n\n"
                    f"Order Number: {order.order_number}\n\n"
                    "Enter this OTP on the payment verification page "
                    "to complete your order.\n\n"
                    "Please do not share this OTP with anyone.\n\n"
                    "Thank you,\n"
                    "Sweet Cake Shop"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            print("OTP EMAIL SENT TO:", email)

        except Exception as email_error:
            print("OTP EMAIL ERROR:", email_error)

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Payment was verified, but the OTP email could not "
                        f"be sent: {email_error}"
                    ),
                },
                status=500,
            )

        # ==============================
        # OPEN OTP PAGE
        # ==============================

        return JsonResponse(
            {
                "success": True,
                "otp_required": True,
                "url": reverse(
                    "shop:verify_payment_otp",
                    args=[order.order_number],
                ),
                "message": "Payment verified. OTP sent to your email.",
            }
        )
        # IMPORTANT:
        # Do NOT mark order PAID yet.
        # OTP must be verified first.

        return JsonResponse({
            "success": True,
            "otp_required": True,
            "url": reverse(
                "shop:verify_payment_otp",
                args=[order.order_number]
            ),
            "message": (
                "Payment verified. "
                "OTP sent to your mobile."
            )
        })

    except Exception as exc:

        print(
            "PAYMENT VERIFICATION ERROR:",
            exc
        )

        return JsonResponse({
            "success": False,
            "error": str(exc)
        }, status=400)

@login_required
def order_success(request, order_number):
    order = get_object_or_404(order_qs(), order_number=order_number, user=request.user)
    return render(request, "shop/success.html", {"order": order})


def order_qs():
    return Order.objects.prefetch_related("items__cake", "notifications")


@login_required
def my_orders(request):
    orders = order_qs().filter(user=request.user)
    return render(request, "shop/orders.html", {"orders": orders})


@login_required
def update_order_status(request, order_number):
    if not request.user.is_staff:
        return JsonResponse({"error": "Staff only"}, status=403)
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    order = get_object_or_404(Order, order_number=order_number)
    new_status = request.POST.get("status", "")
    allowed = dict(Order.STATUS)
    if new_status not in allowed:
        return JsonResponse({"error": "Invalid status"}, status=400)
    order.status = new_status
    order.save(update_fields=["status"])
    event_map = {"BAKING": "baking", "OUT": "out", "DELIVERED": "delivered"}
    if new_status in event_map:
        _notify_order(order, event_map[new_status])
    return redirect("shop:admin_dashboard")


@login_required
def custom_cake(request):
    form = CustomCakeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, "Custom cake request submitted! We will contact you shortly.")
        send_customer_notification(
            user=request.user,
            phone=request.user.profile.phone if hasattr(request.user, "profile") else "",
            message=f"Sweet Cake Shop: Your custom cake request #{obj.pk} was received.",
            channel="SMS",
        ) if getattr(settings, "TWILIO_FROM_NUMBER", "") else None
        return redirect("shop:custom_cake")
    return render(request, "shop/custom_cake.html", {"form": form})


@login_required
def add_review(request, cake_id):
    if request.method != "POST":
        return redirect("shop:detail", slug=get_object_or_404(Cake, id=cake_id).slug)
    cake = get_object_or_404(Cake, id=cake_id)
    rating = int(request.POST.get("rating", 5))
    comment = request.POST.get("comment", "").strip()
    if not 1 <= rating <= 5 or not comment:
        messages.error(request, "Please provide a rating and review.")
        return redirect("shop:detail", slug=cake.slug)
    Review.objects.update_or_create(
        user=request.user, cake=cake,
        defaults={"rating": rating, "comment": comment},
    )
    messages.success(request, "Your review was saved.")
    return redirect("shop:detail", slug=cake.slug)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
        else:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, f"Thanks {name}! Your message has been received.")
            return redirect("shop:contact")
    return render(request, "shop/contact.html")

@login_required
def verify_payment_otp(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user,
    )

    if request.session.get("payment_otp_order") != order.order_number:
        messages.error(request, "This OTP session is not active. Please complete the payment again.")
        return redirect("shop:payment", order_number=order.order_number)

    if request.method == "GET":
        return render(
            request,
            "shop/otp_verify.html",
            {
                "order": order,
            },
        )

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        if not entered_otp:
            return render(
                request,
                "shop/otp_verify.html",
                {
                    "order": order,
                    "error": "Please enter OTP.",
                },
            )

        if order.otp_verified:
            return redirect(
                "shop:order_success",
                order_number=order.order_number,
            )

        if entered_otp != order.otp:
            return render(
                request,
                "shop/otp_verify.html",
                {
                    "order": order,
                    "error": "Invalid OTP. Please try again.",
                },
            )

        with transaction.atomic():

            order.otp_verified = True
            order.payment_status = "PAID"
            order.status = "PLACED"

            order.save(
                update_fields=[
                    "otp_verified",
                    "payment_status",
                    "status",
                ]
            )

            for item in order.items.select_related("cake"):

                if item.cake.stock < item.quantity:
                    raise ValueError(
                        f"Not enough stock for {item.cake.name}."
                    )

                item.cake.stock -= item.quantity

                item.cake.save(
                    update_fields=["stock"]
                )

        request.session["cart"] = {}
        request.session.pop("payment_otp_order", None)

        try:
            _notify_order(order, "placed")
        except Exception as sms_error:
            print("OTP SMS ERROR:", sms_error)

        return redirect(
            "shop:order_success",
            order_number=order.order_number,
        )

    return JsonResponse(
        {
            "success": False,
            "error": "Invalid request.",
        },
        status=400,
    )

