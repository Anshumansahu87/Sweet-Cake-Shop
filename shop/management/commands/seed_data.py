from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Order, OrderItem
from django.utils.text import slugify
from shop.models import Category, Cake, Coupon

DATA = {
    "Birthday Cakes": [
        (
            "Chocolate Truffle Cake",
            "Rich chocolate sponge covered with smooth chocolate ganache. Perfect for birthdays.",
            699, False, True,
            "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=85",
        ),
        (
            "Red Velvet Cake",
            "Soft red velvet layers with creamy frosting and a beautiful celebration finish.",
            799, False, True,
            "https://images.unsplash.com/photo-1586788224331-947f68671cf1?auto=format&fit=crop&w=900&q=85",
        ),
        (
            "Black Forest Cake",
            "Classic chocolate cake with cream and cherry layers.",
            749, False, False,
            "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?auto=format&fit=crop&w=900&q=85",
        ),
    ],
    "Eggless Cakes": [
        (
            "Eggless Vanilla Cake",
            "Light vanilla sponge with creamy vanilla frosting. 100% eggless.",
            599, True, True,
            "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?auto=format&fit=crop&w=900&q=85",
        ),
        (
            "Eggless Chocolate Cake",
            "Moist eggless chocolate cake with a rich chocolate topping.",
            699, True, False,
            "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?auto=format&fit=crop&w=900&q=85",
        ),
    ],
    "Premium Cakes": [
        (
            "Strawberry Cream Cake",
            "Fresh strawberry-inspired cream cake for special occasions.",
            999, False, True,
            "https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=900&q=85",
        ),
        (
            "Biscoff Celebration Cake",
            "Premium caramel-biscuit inspired cake with a creamy finish.",
            1099, False, False,
            "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=900&q=85",
        ),
    ],
    "Cupcakes": [
        (
            "Chocolate Cupcake Box",
            "Box of delicious chocolate cupcakes for parties and small celebrations.",
            449, False, True,
            "https://images.unsplash.com/photo-1587668178277-295251f900ce?auto=format&fit=crop&w=900&q=85",
        ),
        (
            "Vanilla Cupcake Box",
            "Soft vanilla cupcakes with creamy frosting.",
            399, True, False,
            "https://images.unsplash.com/photo-1576618148400-cd9a8b3d9b7c?auto=format&fit=crop&w=900&q=85",
        ),
    ],
}

class Command(BaseCommand):
    help = "Create demo categories and cakes."

    def handle(self, *args, **kwargs):
        for category_name, cakes in DATA.items():
            category, _ = Category.objects.get_or_create(
                slug=slugify(category_name),
                defaults={"name": category_name},
            )

            for name, description, price, eggless, featured, image_url in cakes:
                Cake.objects.update_or_create(
                    slug=slugify(name),
                    defaults={
                        "category": category,
                        "name": name,
                        "description": description,
                        "price": price,
                        "stock": 25,
                        "eggless": eggless,
                        "featured": featured,
                        "image_url": image_url,
                    },
                )

        Coupon.objects.update_or_create(code="SWEET10", defaults={"discount_percent": 10, "min_order": 999, "active": True})

        # Local demo account and sample orders for the internship UI/dashboard.
        demo, created = User.objects.get_or_create(username="demo_user", defaults={"email":"demo@sweetcakeshop.local"})
        if created:
            demo.set_password("Demo@12345")
            demo.save()

        cakes = list(Cake.objects.order_by("id")[:3])
        if cakes:
            samples = [
                ("SCDEMO1003", "Anshuman Sahu", cakes[:1], "DELIVERED", "COD"),
                ("SCDEMO1002", "Rahul Kumar", cakes[1:2], "OUT", "PAID"),
                ("SCDEMO1001", "Priya Singh", cakes[2:3], "CANCELLED", "COD"),
            ]
            for number, customer, chosen, status, payment in samples:
                order, created_order = Order.objects.get_or_create(
                    order_number=number, defaults={
                        "user": demo, "customer_name": customer, "phone":"9876543210",
                        "address":"123, Bistupur, Jamshedpur", "city":"Jamshedpur", "pincode":"831001",
                        "total": chosen[0].price if chosen else 0, "status":status,
                        "payment_status":payment, "payment_method":payment,
                    })
                if created_order and chosen:
                    OrderItem.objects.create(order=order, cake=chosen[0], quantity=1, price=chosen[0].price)

        self.stdout.write(self.style.SUCCESS("Demo cake data and optional dashboard demo data created successfully."))
