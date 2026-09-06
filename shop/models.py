from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cake(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="cakes"
    )
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    eggless = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    image_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="cakes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveIntegerField(default=10)
    min_order = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class CustomCakeRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_cake_requests"
    )
    message_on_cake = models.CharField(max_length=120)
    flavour = models.CharField(max_length=80)
    size = models.CharField(max_length=40)
    theme = models.CharField(max_length=120, blank=True)
    delivery_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Custom cake #{self.pk} - {self.user.username}"


class Order(models.Model):
    STATUS = [
        ("PLACED", "Order Placed"),
        ("BAKING", "Being Baked"),
        ("OUT", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT = [
        ("COD", "Cash on Delivery"),
        ("PAID", "Paid"),
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(max_length=24, unique=True)

    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)

    address = models.TextField()
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)

    delivery_date = models.DateField(null=True, blank=True)
    delivery_slot = models.CharField(max_length=40, blank=True)

    custom_message = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    subtotal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    coupon_code = models.CharField(max_length=30, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PLACED"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT,
        default="PENDING"
    )

    payment_method = models.CharField(
        max_length=20,
        default="COD"
    )

    # Razorpay fields
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True
    )

    # Email OTP fields
    otp = models.CharField(
        max_length=6,
        blank=True
    )

    otp_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    cake = models.ForeignKey(
        Cake,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.order.order_number} - {self.cake.name}"


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cake_reviews"
    )

    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cake"],
                name="one_review_per_user_cake"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cake.name} - {self.rating}/5"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"