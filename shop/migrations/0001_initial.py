from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("discount_percent", models.PositiveIntegerField(default=10)),
                ("min_order", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cake",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("stock", models.PositiveIntegerField(default=10)),
                ("eggless", models.BooleanField(default=False)),
                ("featured", models.BooleanField(default=False)),
                ("image_url", models.URLField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="cakes/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cakes", to="shop.category")),
            ],
            options={"ordering": ["-featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="CustomCakeRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message_on_cake", models.CharField(max_length=120)),
                ("flavour", models.CharField(max_length=80)),
                ("size", models.CharField(max_length=40)),
                ("theme", models.CharField(blank=True, max_length=120)),
                ("delivery_date", models.DateField()),
                ("notes", models.TextField(blank=True)),
                ("status", models.CharField(default="NEW", max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="custom_cake_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_number", models.CharField(max_length=24, unique=True)),
                ("customer_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=80)),
                ("pincode", models.CharField(max_length=10)),
                ("delivery_date", models.DateField(blank=True, null=True)),
                ("delivery_slot", models.CharField(blank=True, max_length=40)),
                ("custom_message", models.CharField(blank=True, max_length=120)),
                ("notes", models.TextField(blank=True)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("discount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("total", models.DecimalField(decimal_places=2, max_digits=8)),
                ("coupon_code", models.CharField(blank=True, max_length=30)),
                ("status", models.CharField(choices=[("PLACED","Order Placed"),("BAKING","Being Baked"),("OUT","Out for Delivery"),("DELIVERED","Delivered"),("CANCELLED","Cancelled")], default="PLACED", max_length=20)),
                ("payment_status", models.CharField(choices=[("COD","Cash on Delivery"),("PAID","Paid"),("PENDING","Pending"),("FAILED","Failed")], default="PENDING", max_length=20)),
                ("payment_method", models.CharField(default="COD", max_length=20)),
                ("razorpay_order_id", models.CharField(blank=True, max_length=100)),
                ("razorpay_payment_id", models.CharField(blank=True, max_length=100)),
                ("razorpay_signature", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("cake", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.cake")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order")),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveIntegerField(default=5)),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("cake", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="shop.cake")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cake_reviews", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("channel", models.CharField(choices=[("SMS","SMS"),("WHATSAPP","WhatsApp")], max_length=12)),
                ("status", models.CharField(choices=[("SENT","Sent"),("DEMO","Demo / Not Configured"),("FAILED","Failed")], default="DEMO", max_length=20)),
                ("phone", models.CharField(max_length=20)),
                ("message", models.TextField()),
                ("provider_id", models.CharField(blank=True, max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="notifications", to="shop.order")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(fields=("user","cake"), name="one_review_per_user_cake"),
        ),
    ]
