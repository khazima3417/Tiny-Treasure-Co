import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import (
    Category, Product, BoxFinish, AtelierItem,
    Cart, CartItem, Order, OrderItem, ContactMessage, Customer
)


class StoreTestSuite(TestCase):
    def setUp(self):
        self.client = Client()

        # Categories
        self.cat_birthdays = Category.objects.create(name='Birthdays', slug='birthdays', icon='cake')
        self.cat_besties = Category.objects.create(name='Best Friends', slug='best-friends', icon='favorite')

        # Products
        self.prod_bestie = Product.objects.create(
            name='Mini Bestie Box',
            slug='mini-bestie-box',
            category=self.cat_besties,
            price=Decimal('999.00'),
            short_description='Best friend petite gift hamper',
            description='A sweet reminder of cherished bonds.',
            items_included='Silk Scrunchie, Dainty Bracelet',
            is_featured=True,
            is_active=True
        )

        self.prod_birthday = Product.objects.create(
            name='Birthday Surprise Box',
            slug='birthday-surprise-box',
            category=self.cat_birthdays,
            price=Decimal('1999.00'),
            short_description='Signature birthday box with candle',
            description='Our most loved birthday gift hamper.',
            items_included='Vanilla Candle, Rose Quartz Pendant',
            is_featured=True,
            is_bestseller=True,
            is_active=True
        )

        # Box Finishes
        self.finish_blush = BoxFinish.objects.create(
            name='Blush Silk',
            price=Decimal('499.00'),
            color_hex='#f6dadc',
            text_color='#825057'
        )

        # Atelier Items
        self.item_candle = AtelierItem.objects.create(
            name='Vanilla Blossom Soy Candle',
            price=Decimal('450.00'),
            stock=50
        )
        self.item_mask = AtelierItem.objects.create(
            name='Silk Sleep Eye Mask',
            price=Decimal('350.00'),
            stock=50
        )

    # 1. Product Display & Catalog
    def test_homepage_product_display(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mini Bestie Box')
        self.assertContains(response, 'Birthday Surprise Box')
        self.assertContains(response, '999')

    def test_shop_catalog_and_category_filter(self):
        response = self.client.get(reverse('shop') + '?occasion=birthdays')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.prod_birthday, response.context['products'])
        self.assertNotIn(self.prod_bestie, response.context['products'])

    def test_shop_search_filter(self):
        response = self.client.get(reverse('shop') + '?q=Bestie')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.prod_bestie, response.context['products'])
        self.assertNotIn(self.prod_birthday, response.context['products'])

    def test_shop_price_filter(self):
        response = self.client.get(reverse('shop') + '?price=under-1500')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.prod_bestie, response.context['products'])
        self.assertNotIn(self.prod_birthday, response.context['products'])

    # 2. Shopping Cart Operations
    def test_add_standard_product_to_cart(self):
        response = self.client.post(reverse('add_to_cart'), {
            'product_id': self.prod_bestie.id,
            'quantity': 2,
            'seal_color': 'Rose Gold',
            'card_message': 'Happy Birthday Sara!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to checkout
        
        # Verify cart in DB
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.get_total_items(), 2)
        self.assertEqual(cart.get_subtotal(), Decimal('1998.00'))
        # Subtotal < 3000, so shipping is 250
        self.assertEqual(cart.get_shipping_fee(), Decimal('250.00'))
        self.assertEqual(cart.get_total(), Decimal('2248.00'))

    def test_add_custom_box_to_cart(self):
        response = self.client.post(reverse('add_custom_box'), {
            'occasion': 'Birthday',
            'box_finish_id': self.finish_blush.id,
            'tier_name': 'Classic Edit',  # Base: 1999
            'recipient_name': 'Areeba Malik',
            'sender_name': 'Sana',
            'card_message': 'Best wishes for your special day!',
            'seal_color': 'Antique Rose',
            'ribbon_material': 'Double-faced Satin Rose',
            'item_ids': [self.item_candle.id, self.item_mask.id],  # 450 + 350 = 800
        })
        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        # Expected price: Tier 1999 + Finish 499 + Items (450 + 350 = 800) = 3298
        custom_item = cart.items.first()
        self.assertEqual(custom_item.unit_price, Decimal('3298.00'))
        # Since >= 3000, shipping is free!
        self.assertEqual(cart.get_shipping_fee(), Decimal('0.00'))
        self.assertEqual(cart.get_total(), Decimal('3298.00'))

    def test_cart_quantity_update_ajax(self):
        # Add item first
        self.client.post(reverse('add_to_cart'), {'product_id': self.prod_bestie.id, 'quantity': 1})
        cart = Cart.objects.first()
        item = cart.items.first()

        # Increase quantity via AJAX
        response = self.client.post(reverse('update_cart_quantity'), {
            'cart_item_id': item.id,
            'action': 'increase'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_item_count'], 2)

    # 3. User Authentication
    def test_customer_registration_and_login(self):
        reg_response = self.client.post(reverse('register'), {
            'username': 'ayesha_k',
            'full_name': 'Ayesha Khan',
            'email': 'ayesha@example.com',
            'phone': '03009876543',
            'password': 'safePassword123',
            'confirm_password': 'safePassword123',
        })
        self.assertEqual(reg_response.status_code, 302)

        user = User.objects.filter(username='ayesha_k').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.customer_profile.phone, '03009876543')

        # Test Logout
        self.client.get(reverse('logout'))

        # Test Login
        login_response = self.client.post(reverse('login'), {
            'username': 'ayesha@example.com',
            'password': 'safePassword123'
        })
        self.assertEqual(login_response.status_code, 302)

    # 4. Checkout and Order Creation with Cash on Delivery
    def test_checkout_and_order_creation_cod(self):
        # Add product to cart
        self.client.post(reverse('add_to_cart'), {'product_id': self.prod_birthday.id, 'quantity': 2})
        # 1999 * 2 = 3998 (free shipping)

        response = self.client.post(reverse('cart_checkout'), {
            'customer_name': 'Hina Bilal',
            'customer_email': 'hina@example.com',
            'customer_phone': '03211234567',
            'is_surprise_gift': True,
            'recipient_name': 'Zara Ali',
            'recipient_address': 'House 12, Street 4, F-7/3',
            'recipient_city': 'Islamabad',
            'recipient_postal': '44000',
            'card_message': 'Sending love on your 25th birthday!',
            'wax_seal_preference': 'Rose Gold',
            'delivery_instructions': 'Leave with security guard',
            'payment_method': 'cod',
        })

        # Should redirect to order confirmation
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertTrue(order.order_number.startswith('TGE-PK-'))
        self.assertEqual(order.payment_method, 'cod')
        self.assertEqual(order.subtotal, Decimal('3998.00'))
        self.assertEqual(order.shipping_fee, Decimal('0.00'))
        self.assertEqual(order.total_price, Decimal('3998.00'))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().item_name, 'Birthday Surprise Box')

        # Cart should be empty now
        cart = Cart.objects.first()
        self.assertEqual(cart.items.count(), 0)

    # 5. Contact Form Submission
    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Hamza Sheikh',
            'email': 'hamza@example.com',
            'phone': '03335557777',
            'subject': 'Corporate Hamper Inquiry (50 Boxes)',
            'message': 'We would like to order 50 customized gift hampers for our annual gala in Lahore.'
        })
        self.assertEqual(response.status_code, 302)

        msg = ContactMessage.objects.filter(email='hamza@example.com').first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.subject, 'Corporate Hamper Inquiry (50 Boxes)')
        self.assertFalse(msg.is_read)
