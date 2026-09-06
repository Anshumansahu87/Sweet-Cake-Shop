def shop_context(request):
    cart = request.session.get("cart", {})
    wishlist = request.session.get("wishlist", [])
    return {
        "cart_count": sum(int(q) for q in cart.values()),
        "wishlist_count": len(wishlist),
    }
