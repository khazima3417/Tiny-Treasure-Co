import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import (
    Category, Product, BoxFinish, AtelierItem,
    Customer, ShippingAddress, Cart, CartItem,
    Order, OrderItem, ContactMessage, NewsletterSubscriber
)
from .forms import CustomerRegistrationForm, CustomerLoginForm, ContactForm
from .context_processors import get_or_create_cart


def home_view(request):
    """Boutique Homepage showcasing featured gift hampers, atelier teaser, and reviews."""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    if not featured_products.exists():
        featured_products = Product.objects.filter(is_active=True)[:4]

    categories = Category.objects.filter(is_active=True)
    box_finishes = BoxFinish.objects.filter(is_active=True)
    atelier_items = AtelierItem.objects.filter(is_active=True)[:6]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'box_finishes': box_finishes,
        'atelier_items': atelier_items,
        'page_title': 'Curated With Love • Bespoke Boxes',
    }
    return render(request, 'store/home.html', context)


def shop_view(request):
    """Catalog page with filtering by occasion, price range, search, and sorting."""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Occasion / Category filter
    occasion = request.GET.get('occasion', 'all')
    if occasion and occasion != 'all':
        products = products.filter(Q(category__slug=occasion) | Q(category__name__iexact=occasion.replace('-', ' ')))

    # Price filter
    price_tier = request.GET.get('price', 'all')
    if price_tier == 'under-1500':
        products = products.filter(price__lt=1500)
    elif price_tier == '1500-2500':
        products = products.filter(price__gte=1500, price__lte=2500)
    elif price_tier == 'over-2500':
        products = products.filter(price__gt=2500)

    # Search keyword
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(items_included__icontains=query)
        )

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'low-high':
        products = products.order_by('price')
    elif sort == 'high-low':
        products = products.order_by('-price')
    elif sort == 'bestseller':
        products = products.order_by('-is_bestseller', '-rating')
    else:
        products = products.order_by('-is_featured', 'price')

    context = {
        'products': products,
        'categories': categories,
        'active_occasion': occasion,
        'active_price': price_tier,
        'active_sort': sort,
        'search_query': query,
        'products_count': products.count(),
        'page_title': 'Shop All Curated Gift Boxes',
    }
    return render(request, 'store/shop.html', context)


def product_detail_view(request, slug):
    """View a specific gift hamper by filtering in shop catalog."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return redirect(f"/shop/?q={product.name}")


def customize_view(request):
    """Interactive Atelier 5-step box builder."""
    occasions = Category.objects.filter(is_active=True)
    box_finishes = BoxFinish.objects.filter(is_active=True)
    atelier_items = AtelierItem.objects.filter(is_active=True)

    context = {
        'occasions': occasions,
        'box_finishes': box_finishes,
        'atelier_items': atelier_items,
        'page_title': 'Customize Your Box • Atelier Builder',
    }
    return render(request, 'store/customize.html', context)


@require_POST
def add_to_cart_view(request):
    """Add a standard curated gift box to the shopping cart."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    seal_color = request.POST.get('seal_color', 'Rose Gold')
    card_message = request.POST.get('card_message', '').strip()
    direct_recipient = request.POST.get('direct_recipient') in ['true', 'on', '1', True]

    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)

    # Check if this exact product is already in the cart with the same message
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        seal_color=seal_color,
        card_message=card_message,
        defaults={
            'unit_price': product.price,
            'quantity': quantity,
            'direct_recipient': direct_recipient
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to your cart.",
            'cart_item_count': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_total': str(cart.get_total()),
        })

    messages.success(request, f"'{product.name}' was added to your curated gift basket.")
    return redirect('cart_checkout')


@require_POST
def add_custom_box_view(request):
    """Handle custom bespoke atelier box addition with server-side validation."""
    occasion = request.POST.get('occasion', 'Birthday')
    box_finish_id = request.POST.get('box_finish_id')
    tier_name = request.POST.get('tier_name', 'Classic Edit')
    recipient_name = request.POST.get('recipient_name', '').strip()
    sender_name = request.POST.get('sender_name', '').strip()
    card_message = request.POST.get('card_message', '').strip()
    seal_color = request.POST.get('seal_color', 'Antique Rose')
    ribbon_material = request.POST.get('ribbon_material', 'Double-faced Satin Rose')
    
    # Selected items IDs
    item_ids = request.POST.getlist('item_ids')
    if not item_ids and request.POST.get('item_ids'):
        try:
            item_ids = json.loads(request.POST.get('item_ids'))
        except Exception:
            item_ids = [request.POST.get('item_ids')]

    # Calculate exact price server-side
    tier_base_prices = {
        'Mini Delight': Decimal('999.00'),
        'Classic Edit': Decimal('1999.00'),
        'Luxury Keepsake': Decimal('3499.00'),
    }
    base_price = tier_base_prices.get(tier_name, Decimal('1999.00'))

    box_finish = None
    finish_price = Decimal('499.00')
    finish_name = 'Blush Silk'
    if box_finish_id:
        try:
            box_finish = BoxFinish.objects.get(id=box_finish_id)
            finish_price = box_finish.price
            finish_name = box_finish.name
        except BoxFinish.DoesNotExist:
            pass

    # Sum verified atelier items
    selected_items_objects = AtelierItem.objects.filter(id__in=item_ids, is_active=True)
    items_total = sum(item.price for item in selected_items_objects)
    items_names = [item.name for item in selected_items_objects]

    # Total unit price for this custom curation
    unit_price = base_price + finish_price + items_total

    custom_details = {
        'occasion': occasion,
        'finish': finish_name,
        'tier': tier_name,
        'items': items_names,
        'recipient': recipient_name,
        'sender': sender_name,
        'ribbon': ribbon_material,
    }

    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.create(
        cart=cart,
        product=None,
        custom_title=f"Custom {tier_name} ({finish_name})",
        custom_details=json.dumps(custom_details),
        unit_price=unit_price,
        quantity=1,
        seal_color=seal_color,
        card_message=card_message,
        direct_recipient=bool(recipient_name),
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
        return JsonResponse({
            'success': True,
            'message': f"Custom {tier_name} added to your cart.",
            'cart_item_count': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_total': str(cart.get_total()),
        })

    messages.success(request, f"Your bespoke {tier_name} box has been added to your cart.")
    return redirect('cart_checkout')


@require_POST
def update_cart_quantity_view(request):
    """Update item quantity or remove item via AJAX."""
    cart_item_id = request.POST.get('cart_item_id')
    action = request.POST.get('action')  # 'increase', 'decrease', 'remove'
    cart = get_or_create_cart(request)

    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete()

    return JsonResponse({
        'success': True,
        'cart_item_count': cart.get_total_items(),
        'item_subtotal': str(cart_item.get_subtotal()) if cart_item.id else '0.00',
        'cart_subtotal': str(cart.get_subtotal()),
        'cart_shipping': str(cart.get_shipping_fee()),
        'cart_total': str(cart.get_total()),
    })


def remove_from_cart_view(request, item_id):
    """Remove item from cart and redirect."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    name = cart_item.get_display_title()
    cart_item.delete()
    messages.info(request, f"Removed '{name}' from your cart.")
    return redirect('cart_checkout')


def cart_checkout_view(request):
    """Integrated Cart review and Checkout page."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    # Pre-populate sender details if user is logged in
    sender_name = ''
    sender_email = ''
    sender_phone = ''
    if request.user.is_authenticated:
        sender_email = request.user.email
        if hasattr(request.user, 'customer_profile'):
            profile = request.user.customer_profile
            sender_name = profile.full_name
            sender_phone = profile.phone

    if request.method == 'POST':
        if not cart_items.exists():
            messages.error(request, "Your cart is empty. Please add items before checking out.")
            return redirect('shop')

        # Collect form fields
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        is_surprise_gift = request.POST.get('is_surprise_gift') in ['true', 'on', '1', True]
        recipient_name = request.POST.get('recipient_name', '').strip()
        recipient_address = request.POST.get('recipient_address', '').strip()
        recipient_city = request.POST.get('recipient_city', 'Islamabad').strip()
        recipient_postal = request.POST.get('recipient_postal', '').strip()
        card_message = request.POST.get('card_message', '').strip()
        wax_seal = request.POST.get('wax_seal_preference', 'Rose Gold').strip()
        delivery_notes = request.POST.get('delivery_instructions', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        if not customer_name or not customer_email or not customer_phone or not recipient_name or not recipient_address:
            messages.error(request, "Please fill in all required sender and delivery address fields.")
            return redirect('cart_checkout')

        # Recalculate totals on server
        subtotal = cart.get_subtotal()
        shipping_fee = cart.get_shipping_fee()
        total_price = subtotal + shipping_fee

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            is_surprise_gift=is_surprise_gift,
            recipient_name=recipient_name,
            recipient_address=recipient_address,
            recipient_city=recipient_city,
            recipient_postal=recipient_postal,
            card_message=card_message,
            wax_seal_preference=wax_seal,
            delivery_instructions=delivery_notes,
            payment_method=payment_method,
            payment_status='pending',
            status='received',
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total_price=total_price,
        )

        # Create Order Items from Cart Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                item_name=item.get_display_title(),
                item_details=item.get_display_subtitle(),
                price=item.unit_price,
                quantity=item.quantity,
                subtotal=item.get_subtotal(),
            )

        # Clear the cart items
        cart_items.delete()

        # Update or create Customer profile if logged in
        if request.user.is_authenticated:
            Customer.objects.update_or_create(
                user=request.user,
                defaults={
                    'full_name': customer_name,
                    'email': customer_email,
                    'phone': customer_phone,
                    'address': recipient_address,
                    'city': recipient_city,
                }
            )

        messages.success(request, f"Order #{order.order_number} confirmed! Our atelier is preparing your gifts.")
        return redirect('order_confirmation', order_number=order.order_number)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'sender_name': sender_name,
        'sender_email': sender_email,
        'sender_phone': sender_phone,
        'page_title': 'Cart & Boutique Checkout',
    }
    return render(request, 'store/cart_checkout.html', context)


def order_confirmation_view(request, order_number):
    """Order confirmation and receipt display."""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
        'order_items': order.items.all(),
        'page_title': f"Order #{order.order_number} Confirmed",
    }
    return render(request, 'store/order_confirmation.html', context)


def contact_view(request):
    """Customer Concierge and Contact form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shukriya! Your message has been received by our Atelier Concierge. We will reply promptly via WhatsApp or email.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Contact Atelier Concierge',
    }
    return render(request, 'store/contact.html', context)


def about_view(request):
    """About us story and artisan process."""
    context = {
        'page_title': 'Our Atelier Story • Handcrafted in Pakistan',
    }
    return render(request, 'store/about.html', context)


@require_POST
def newsletter_view(request):
    """Newsletter subscription via form."""
    email = request.POST.get('email', '').strip()
    if email:
        NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, "Welcome to The Atelier Circle! Enjoy 10% off your first bespoke order.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_view(request):
    """Customer account registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create customer profile
            Customer.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )

            # Log user in
            login(request, user)
            messages.success(request, f"Welcome to Tiny Treasure Co., {user.username}! Your account is active.")
            return redirect('home')
    else:
        form = CustomerRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Create Customer Account',
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """Customer login with username or email."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Allow login via username or email
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = CustomerLoginForm()

    context = {
        'form': form,
        'page_title': 'Sign In to Your Account',
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """Customer logout."""
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('home')


@login_required
def profile_view(request):
    """Customer profile and past orders."""
    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.get_full_name() or request.user.username, 'email': request.user.email}
    )
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'customer': customer,
        'orders': orders,
        'page_title': 'My Account & Orders',
    }
    return render(request, 'accounts/profile.html', context)
