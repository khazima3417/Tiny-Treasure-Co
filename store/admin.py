from django.contrib import admin
from .models import (
    Category, Product, BoxFinish, AtelierItem,
    Customer, ShippingAddress, Cart, CartItem,
    Order, OrderItem, ContactMessage, NewsletterSubscriber
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'tag', 'is_featured', 'is_bestseller', 'is_active')
    list_filter = ('category', 'is_featured', 'is_bestseller', 'is_active')
    list_editable = ('price', 'stock', 'is_featured', 'is_bestseller', 'is_active')
    search_fields = ('name', 'description', 'items_included')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'tag', 'is_active')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'original_price', 'stock')
        }),
        ('Descriptions & Items Included', {
            'fields': ('short_description', 'description', 'items_included', 'box_color')
        }),
        ('Media & Badges', {
            'fields': ('image', 'image_url', 'rating', 'reviews_count', 'is_featured', 'is_bestseller')
        }),
    )


@admin.register(BoxFinish)
class BoxFinishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'color_hex', 'text_color', 'is_active')
    list_editable = ('price', 'color_hex', 'is_active')


@admin.register(AtelierItem)
class AtelierItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active')
    list_editable = ('price', 'stock', 'is_active')
    search_fields = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'city', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'city')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('recipient_name', 'phone', 'city', 'is_default', 'created_at')
    list_filter = ('city', 'is_default')
    search_fields = ('recipient_name', 'phone', 'street_address')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'custom_title', 'unit_price', 'quantity', 'seal_color', 'card_message')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'user', 'get_total_items', 'created_at', 'updated_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'recipient_city', 'payment_method', 'payment_status', 'status', 'total_price', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'status', 'recipient_city', 'created_at')
    list_editable = ('payment_status', 'status')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone', 'recipient_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'shipping_fee', 'total_price')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Identification', {
            'fields': ('order_number', 'status', 'created_at')
        }),
        ('Customer (Sender)', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Recipient & Delivery', {
            'fields': ('is_surprise_gift', 'recipient_name', 'recipient_address', 'recipient_city', 'recipient_postal', 'delivery_instructions')
        }),
        ('Keepsake Card & Wax Seal', {
            'fields': ('card_message', 'wax_seal_preference')
        }),
        ('Payment & Totals', {
            'fields': ('payment_method', 'payment_status', 'subtotal', 'shipping_fee', 'total_price')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
