from .models import Cart, Category
from decimal import Decimal


def get_or_create_cart(request):
    """Retrieve existing cart or create a new one based on session or user."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            # Check if there is an existing session cart to adopt
            cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if cart:
                cart.user = request.user
                cart.save()
            else:
                cart = Cart.objects.create(user=request.user, session_key=session_key)
    else:
        cart = Cart.objects.filter(session_key=session_key).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key)

    return cart


def cart_context(request):
    """Context processor providing cart state and active categories across all pages."""
    try:
        cart = get_or_create_cart(request)
        item_count = cart.get_total_items()
        subtotal = cart.get_subtotal()
        shipping = cart.get_shipping_fee()
        total = cart.get_total()
    except Exception:
        cart = None
        item_count = 0
        subtotal = Decimal('0.00')
        shipping = Decimal('0.00')
        total = Decimal('0.00')

    categories = Category.objects.filter(is_active=True)

    return {
        'cart': cart,
        'cart_item_count': item_count,
        'cart_subtotal': subtotal,
        'cart_shipping': shipping,
        'cart_total': total,
        'nav_categories': categories,
        'STORE_NAME': 'Tiny Treasure Co.',
        'BRAND_NAME': 'The Gift Edit',
    }
