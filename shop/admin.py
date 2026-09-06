from django.contrib import admin
from .models import (
    Category, Cake, Coupon, CustomCakeRequest, Order, OrderItem,
    Review, ContactMessage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "eggless", "featured")
    list_filter = ("category", "eggless", "featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "min_order", "active")
    list_filter = ("active",)
    search_fields = ("code",)


@admin.register(CustomCakeRequest)
class CustomCakeRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "flavour", "size", "delivery_date", "status", "created_at")
    list_filter = ("status", "flavour", "size")
    search_fields = ("user__username", "message_on_cake", "theme")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "customer_name", "total", "status",
        "payment_status", "payment_method", "delivery_date", "created_at"
    )
    list_filter = ("status", "payment_status", "payment_method")
    search_fields = ("order_number", "customer_name", "phone")
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("cake", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("cake__name", "user__username", "comment")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")


