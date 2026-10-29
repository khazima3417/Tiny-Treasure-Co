import json
import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Occasions and collections (e.g. Birthdays, Best Friends, Anniversaries)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='cake', help_text="Google Material Symbols icon name")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Curated luxury gift hampers and signature boxes."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.URLField(max_length=1000, blank=True, help_text="CDN or external image URL")
    stock = models.PositiveIntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    tag = models.CharField(max_length=100, blank=True, help_text="Badge text (e.g. Bestseller, Petite Edition)")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    reviews_count = models.PositiveIntegerField(default=48)
    items_included = models.TextField(blank=True, help_text="Comma-separated or newline-separated item list")
    box_color = models.CharField(max_length=50, blank=True, default="Blush Pink")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'price']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/static/images/blush_box_flatlay.png'

    def get_items_list(self):
        if not self.items_included:
            return []
        lines = [item.strip() for item in self.items_included.replace('\n', ',').split(',') if item.strip()]
        return lines

    def __str__(self):
        return f"{self.name} (PKR {self.price})"


class BoxFinish(models.Model):
    """Keepsake box finish for the customizer atelier."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=499.00)
    color_hex = models.CharField(max_length=20, default="#f6dadc")
    text_color = models.CharField(max_length=20, default="#825057")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Box Finishes'

    def __str__(self):
        return f"{self.name} (+PKR {self.price})"


class AtelierItem(models.Model):
    """Individual gift items that can be added into a bespoke box."""
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=1000, blank=True)
    stock = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.name} (+PKR {self.price})"


class Customer(models.Model):
    """Customer profile linked to Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_profile')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, default='Islamabad')
    postal_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or (self.user.username if self.user else "Anonymous Customer")


class ShippingAddress(models.Model):
    """Saved delivery destination for orders."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='shipping_addresses')
    recipient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    street_address = models.TextField()
    city = models.CharField(max_length=100, default='Islamabad')
    postal_code = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f"{self.recipient_name} - {self.city}"


class Cart(models.Model):
    """Shopping cart backed by session or logged-in user."""
    session_key = models.CharField(max_length=60, null=True, blank=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_shipping_fee(self):
        subtotal = self.get_subtotal()
        if subtotal == 0:
            return Decimal('0.00')
        # Free shipping for orders PKR 3,000 and above
        if subtotal >= Decimal('3000.00'):
            return Decimal('0.00')
        return Decimal('250.00')

    def get_total(self):
        return self.get_subtotal() + self.get_shipping_fee()

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart #{self.id} ({self.get_total_items()} items)"


class CartItem(models.Model):
    """Item within cart - can be a standard product or custom bespoke curation."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    custom_title = models.CharField(max_length=200, blank=True)
    custom_details = models.TextField(blank=True, help_text="Stored details (JSON or text)")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    seal_color = models.CharField(max_length=50, blank=True, default='Rose Gold')
    card_message = models.TextField(blank=True)
    direct_recipient = models.BooleanField(default=False)

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def get_display_title(self):
        if self.product:
            return self.product.name
        return self.custom_title or "Bespoke Custom Box"

    def get_display_image(self):
        if self.product:
            return self.product.get_image_url()
        return '/static/images/blush_box_flatlay.png'

    def get_display_subtitle(self):
        if self.product:
            items = self.product.get_items_list()
            return " • ".join(items[:4]) if items else self.product.short_description
        if self.custom_details:
            try:
                data = json.loads(self.custom_details)
                items_str = ", ".join(data.get('items', []))
                return f"{data.get('finish', 'Bespoke Box')} • {items_str}"
            except Exception:
                return self.custom_details
        return "Custom Atelier Curation"

    def __str__(self):
        return f"{self.get_display_title()} x {self.quantity}"


class Order(models.Model):
    """Customer checkout order with server-calculated totals."""
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery (COD)'),
        ('bank', 'Direct Bank Transfer / Raast Instant'),
        ('online', 'Debit/Credit Card (Simulation)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('paid', 'Paid / Verified'),
        ('failed', 'Payment Failed'),
    ]

    STATUS_CHOICES = [
        ('received', 'Order Received'),
        ('handcrafting', 'Handcrafting in Atelier'),
        ('dispatched', 'Dispatched with Courier (TCS / Leopards)'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Customer / Sender Information
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)
    
    # Recipient & Delivery Details
    is_surprise_gift = models.BooleanField(default=True)
    recipient_name = models.CharField(max_length=150)
    recipient_address = models.TextField()
    recipient_city = models.CharField(max_length=100, default='Islamabad')
    recipient_postal = models.CharField(max_length=20, blank=True)
    
    # Handwritten Card Note & Embellishments
    card_message = models.TextField(blank=True)
    wax_seal_preference = models.CharField(max_length=50, blank=True, default="Rose Gold")
    delivery_instructions = models.TextField(blank=True)
    
    # Payment & Status
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='received')
    
    # Pricing Totals (Calculated strictly on the server)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate branded unique order number like TGE-PK-8924
            unique_suffix = uuid.uuid4().hex[:4].upper()
            import random
            rand_digits = random.randint(1000, 9999)
            self.order_number = f"TGE-PK-{rand_digits}"
            # Ensure uniqueness
            while Order.objects.filter(order_number=self.order_number).exists():
                rand_digits = random.randint(1000, 9999)
                self.order_number = f"TGE-PK-{rand_digits}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} (PKR {self.total_price})"


class OrderItem(models.Model):
    """Line items attached to confirmed orders."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=200)
    item_details = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} x {self.quantity} for {self.order.order_number}"


class ContactMessage(models.Model):
    """Customer inquiries submitted via the contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class NewsletterSubscriber(models.Model):
    """Subscribers to The Atelier Circle newsletter."""
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
