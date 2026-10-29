from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, BoxFinish, AtelierItem, Customer


class Command(BaseCommand):
    help = 'Seeds database with real products, categories, box finishes, and atelier items from the frontend.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Tiny Treasure Co. database..."))

        # 1. Create Default Categories
        categories_data = [
            {
                'name': 'Birthdays',
                'slug': 'birthdays',
                'icon': 'cake',
                'description': 'Gifts that celebrate another year of magic.'
            },
            {
                'name': 'Best Friends',
                'slug': 'best-friends',
                'icon': 'favorite',
                'description': 'Sweet tokens for your soul sisters.'
            },
            {
                'name': 'Anniversaries',
                'slug': 'anniversaries',
                'icon': 'auto_stories',
                'description': 'Timeless keepsakes wrapped with care.'
            },
            {
                'name': 'Graduations',
                'slug': 'graduations',
                'icon': 'school',
                'description': 'Honor milestones with refined luxury.'
            },
            {
                'name': 'Self-Care',
                'slug': 'self-care',
                'icon': 'spa',
                'description': 'Thoughtful rest and mindful pampering.'
            },
        ]

        category_objs = {}
        for cat in categories_data:
            obj, created = Category.objects.update_or_create(
                slug=cat['slug'],
                defaults={
                    'name': cat['name'],
                    'icon': cat['icon'],
                    'description': cat['description'],
                    'is_active': True,
                }
            )
            category_objs[cat['slug']] = obj
            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status} Category: {obj.name}")

        # 2. Box Finishes
        finishes_data = [
            {'name': 'Blush Silk', 'price': Decimal('499.00'), 'color_hex': '#f6dadc', 'text_color': '#825057'},
            {'name': 'Warm Cream', 'price': Decimal('499.00'), 'color_hex': '#fbf6ee', 'text_color': '#635d57'},
            {'name': 'Sage Botanical', 'price': Decimal('499.00'), 'color_hex': '#d9e5db', 'text_color': '#425845'},
            {'name': 'Velvet Plum', 'price': Decimal('650.00'), 'color_hex': '#53343c', 'text_color': '#ffd9dd'},
        ]
        for f in finishes_data:
            obj, created = BoxFinish.objects.update_or_create(
                name=f['name'],
                defaults=f
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status} Box Finish: {obj.name}")

        # 3. Atelier Individual Items
        items_data = [
            {
                'name': 'Vanilla Blossom Soy Candle',
                'price': Decimal('450.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBza2I2ADAG2qmIFeLpTCb14fwXeAVm-4GFDBWuAz19Q3w4FlefduENIn8CLm-PSZhre7qiJd_5tUUMhwlz1jk7YRObsLzSQY8R1SLkQ43oCXOVlAPZE0LSn6ztEy1PRr0Ay3BROaEJEZQTPja-qahcxMvE_v1YPy0iRqXJBtJC2lUGfZJWq7lRlXbk4oVK2LZCfc3Gnr19IGL7eNAd_z15JsHjI9gG3W4kbuEyhH2A3S4YdTetl5Nc'
            },
            {
                'name': 'Silk Sleep Eye Mask',
                'price': Decimal('350.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCsb142arVuJfxuBJm0LXlc040Omhe065iJ-eF6AMyJ2Wo8oCs0afsvG_O2aNCjCxaV1P9jqI6nG61ouQ3d7qmnBgqfY04RY8XfvfZN6tDJVFGfCgOh8-gH3dbDZC8_jgchHRddMA9lUX1v4sWrFBdDVLwVZAqtmCXVRKAl6kvj0iTWqQFBckuTondHyaqkhCxJl8m0Wvqlvji320aSDh8Oov9TLcfKkZx_PEwrhDbTvfRNhQlGuBH2'
            },
            {
                'name': 'Rose Quartz Crystal Pendant',
                'price': Decimal('400.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDjW_igxiA320sg1YptYRRxMJjJXR4ssrnacwi3-z1dPOqqC4cXELl3GEu2kdLzoXWRiCt52l3hEIgPxi7C7YFwwFpgUaf1yhtoyzzs7SfiMmsy2r3HGS6pPYZg4kyqY6hxX-IKD88Rr1zFNeEOHkiU3hAXrm5af9JTncezCPqt3pITB0WM6jyk2sYAglexXQb6rJYIpgI1BRfh-lOyJpXI3439mjvh1SaaIN4IoqcMu8Z84-DLO3bu'
            },
            {
                'name': 'Gourmet Bubbly Candies',
                'price': Decimal('320.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDTVU5cIIyK_kG3muFmUmjIRWAaBTgPKhAKEArZPil-j50aXfljn5IDKfogSYtBKwuT8Tfitpin-x8oMSF8_Frb2USGUF1HitELiqOXPXDhlao9FPJbL14Rt_XNcK-83fL2nCftnvTayYrHLwvF4sEI0hOWeLNH-6VKWD_7IfFAEvIm4VUFvTUM12nbamwu35K93sVkR8oMwJwiIsvPqwuK0k6c-UAMIVaUJKWMmJaK0sJNSdVHVcFQ'
            },
            {
                'name': 'Lavender Botanical Mist',
                'price': Decimal('550.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuB1RhljC4k1eIwTZ6ffOaKU-lAw0u7a1O-Y0pItnWUbYpYRBfgmUSMuxhQgWvVdEqnLA_NdLV7Jd2ZdHo4jEsF6os0v8KFgiBPYonJwVoyL3OgVERSLqxEJk0zxb2Igd9y87s_94ZqFwcMt4KEV1pnrzaKTq21KCIYYjnXEqyaZX2PUtMJTyq6IFryKGSQS7dZdLYYA1eJgvjkY2A2jhay-uIAd2iMNaewsc9RFxjnYNtQsmBga8vSu'
            },
            {
                'name': 'Jade Sculpting Roller',
                'price': Decimal('490.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDn2acb_k8EOcPH8LWlgOf4AGYVlZaS_Znb0oKto-KDmJQBX4L7JwyX5PMsO5dYELGRePRMGuJ7Goj11_OurRjjMJXpGZInvOPnI_EgJ5BvwVRLWqK2buUjlw4DPTrH8TQiPEVnrfkcWCc55lsJCkPGIhwlcQruvR141LXa9rW_l-AkZmqe7zGKIlIkHtyebja9MQB2FHejAVk-tjfWA7-JQjT2kQ_Y9voXHhIr3Rv5JGb7jn_cDYY1'
            },
            {
                'name': 'Himalayan Bath Soak with Rose Petals',
                'price': Decimal('380.00'),
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAd2X4sl7HQltMeA6-pW7pe591YaGP5fkuZ22l8pL2dXgZZuOwPZJrr7cj5U5oX84CP4IMbtBT_OculJ6W-oLI9CsBUlQYO_0No0VcXkvMIqEZ0E-bZmOnp1HT0M0RuY5XyKzE-uqaKVUB_I0XcMIzqAuZlRImqLI9oV4FZZ3nwDdGnnqaEBW3hcWnnIZCleFswkqmrpIBn82Ofh_z7avhZRFKudo9LiDHzoquPSlUYMJ6b-Hx3Jx0C'
            },
        ]
        for itm in items_data:
            obj, created = AtelierItem.objects.update_or_create(
                name=itm['name'],
                defaults=itm
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status} Atelier Item: {obj.name}")

        # 4. Catalog Products
        products_data = [
            {
                'name': 'Mini Bestie Box',
                'slug': 'mini-bestie-box',
                'category': category_objs['best-friends'],
                'price': Decimal('999.00'),
                'tag': 'Petite Edition',
                'short_description': 'A sweet reminder of cherished bonds. Thoughtfully proportioned with dainty everyday keepsakes.',
                'description': 'A sweet reminder of cherished bonds. Thoughtfully proportioned with dainty everyday keepsakes. Nestled in crisp crinkle paper and sealed with a personalized handwritten wax seal card.',
                'items_included': 'Silk Scrunchie, Dainty Friendship Bracelet, Scented Soy Tea-Lights, Mini Gold-Foil Card',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuD-D-L9qyhI2rWnOv7jkCKaPhTvv6VGXGUwomn9aDiDYGXcrqEtN2EJmeFL5lvtwryZm-f3SZFDrlrYRO3LQzxwZx17FVj9dufPmpkymiJkBKNYfdr56Gazue3VS6BuHZysGlX0YRLQcVfMUtYDQfFadULzf2d9UG7YivbS1iCFC9QLw9VUSlmHC7ipnFHLjqEjRJ47oH9FQxNEJ6lYwcBh8oCgp5k1QUh6wd9-MWTs82N3Iu6oWcxF',
                'box_color': 'Blush Pink',
                'rating': Decimal('4.9'),
                'reviews_count': 48,
                'is_featured': True,
                'is_bestseller': False,
            },
            {
                'name': 'Birthday Surprise Box',
                'slug': 'birthday-surprise-box',
                'category': category_objs['birthdays'],
                'price': Decimal('1999.00'),
                'tag': 'Bestseller',
                'short_description': 'Our signature birthday hamper featured in elegant pink foil lettering, aromatic candle, and hand-strung gemstone pendant.',
                'description': 'Our most loved birthday gift hamper. Includes an aromatic French vanilla soy candle, hand-strung rose quartz gemstone pendant, celebratory bubbly bites gummies, and a pure silk sleep eye mask wrapped in our signature blush rigid box.',
                'items_included': 'Vanilla Blossom Candle, Rose Quartz Pendant, Champagne Bubbly Candies, Silk Sleep Mask & Greeting Card',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBszzSzHc96YuZPOd0wRQhbTL6be49npbe10C5syVQ0N0CS04bsBtj7cB1yo5phsmJ7N5_wMPai0u4FOlKCPcXYuxRhTDtbrTKhXt9gklRNeviPs61b1GB5yQEhyRbFLjqb9zE8VA9brwXUcQAJjIa3Lhh4W0pO92mJKfTq60dwkjI5QTQ_Gb7Je1V2ttw57komZzEWTdXaQ8s0mbavastc0wg-nC8WKxQ4ws50FTUR__-XrOMg0mS8',
                'box_color': 'Blush Silk',
                'rating': Decimal('5.0'),
                'reviews_count': 124,
                'is_featured': True,
                'is_bestseller': True,
            },
            {
                'name': 'Self-Care Gift Box',
                'slug': 'self-care-gift-box',
                'category': category_objs['self-care'],
                'price': Decimal('2499.00'),
                'tag': 'Staff Pick',
                'short_description': 'Nourish mind and spirit. Natural botanical bath bars, calming French lavender mist, and hand-carved jade massage roller.',
                'description': 'Designed for restorative pampering and mindful moments. Features natural botanical bath bars, calming organic lavender mist, a cooling aventurine jade sculpting roller, and a pure linen eye pillow with personalized card.',
                'items_included': 'Organic Calming Lavender Mist, Jade Facial Roller, Botanical Oatmeal Soap, Pure Linen Eye Pillow & Sealed Note',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDflki4oYrAdyNh1HLCNb3lS_UET1ENime4acq1zSuIKDdxJE_wNp9ZQtJDw1123XvWdqsLLGEOcc0Zq_Q-DGUwyv__LzcXQwE5nSWXsoRL-LiG5lHefZnXqkodV79tRK_aLHjSoDup1jC5lSbYo_U7ixj1CRfJps4y3m8Wd4Wb79vf483LAFATbCyubtG5bz0xPa7To7HAsCrXT0npCqNSPqBtzFgpoLyf01RlUzL9dmUWVK19sRM5',
                'box_color': 'Muted Sage',
                'rating': Decimal('4.9'),
                'reviews_count': 82,
                'is_featured': True,
                'is_bestseller': False,
            },
            {
                'name': 'Sweet Galentine Box',
                'slug': 'sweet-galentine-box',
                'category': category_objs['best-friends'],
                'price': Decimal('1499.00'),
                'tag': 'Friendship',
                'short_description': 'Cozy comfort in a box. Includes handcrafted ceramic mug, Belgian drinking chocolate, and a scented hearth candle.',
                'description': 'A warm hug across miles. Contains an artisan glazed ceramic mug, Belgian drinking chocolate with mini marshmallows, a scented vanilla bean candle, and a gold-embossed love note.',
                'items_included': 'Artisan Ceramic Mug, Gourmet Hot Cocoa, Vanilla Bean Candle, Heart Wax Card',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDJ_-OgTjlYfkIH9g7PK0_A-7EqPdM1HNdy71-PJJYmko2lorBwFRDbb0MjuoEbnu1QTGZv_-EEfbemB2HcbglGuBvHdK4tuADVqKnjXmLrgOl8srCt0Hn926gYCIgWgrt3AqRa3Ci9ZwX1NAcqaMg9OuI2YAZLg-_tT7a7x_fT_eGaGgdyc3-vikhdN1zABAYck4DM7p3sCypT7UZcpObvl-yulEqgU6U0HIoQ1BGXM9OqGrgRk3F1',
                'box_color': 'Ivory Cream',
                'rating': Decimal('4.8'),
                'reviews_count': 37,
                'is_featured': False,
                'is_bestseller': False,
            },
            {
                'name': 'Golden Milestone Box',
                'slug': 'golden-milestone-box',
                'category': category_objs['graduations'],
                'price': Decimal('2999.00'),
                'tag': 'Celebration',
                'short_description': 'Honor life\'s crowning moments. An executive collection composed for ambitious graduates and new beginnings.',
                'description': 'An executive celebration collection composed for ambitious graduates, promotions, and life milestones. Features a weighty champagne gold pen, linen hardcover blank journal, amber jar scented candle, and gold-leaf card.',
                'items_included': 'Rose Gold Heavy Pen, Hardcover Journal, Scented Candle, Gilded Card',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDn-73abNEZ7Zd5gdioOPXVkgWKwyVvqYTCu10M0o5IArsL_8kpfMQnMMPq8-HhpkR_KcboA24cRJNvMkzy5S7aR8HjQk6_uFtP5Gs5acrpUCQymq0qSQTMO1y3dkR0jAxspd2HylF57-9vr1ei1y9le7rhYSqSFBqQV_nGJaS2TN3upZ4zDft3wq7YsapWuuzQjTYJW_IB25XKnvZvFQpQ8Oo1H-iFsj4qh6v1hdhFmlEDQPd2_vHK',
                'box_color': 'Warm Cream',
                'rating': Decimal('5.0'),
                'reviews_count': 59,
                'is_featured': False,
                'is_bestseller': False,
            },
            {
                'name': 'Premium Celebration Box',
                'slug': 'premium-celebration-box',
                'category': category_objs['anniversaries'],
                'price': Decimal('3499.00'),
                'tag': 'Heirloom Luxury',
                'short_description': 'Our grandest gesture. Wrapped with flowing French satin ribbons, debossed keepsake branding, and imported confectionery.',
                'description': 'Our crowning luxury gesture. Enveloped inside an oversized rigid magnetic trunk with double-faced French satin ribbon, containing imported French fragrance mist, an embroidered velvet cosmetics pouch, gold-plated pen, and artisan Belgian chocolate truffles.',
                'items_included': 'French Fragrance Mist, Velvet Keepsake Pouch, Luxury Ballpoint, Artisan Truffles',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA5vSmXtc1SQ4LPqIg6XlOOpekNLWt1CL3gnpY-B8h8lDhA9QZD3fpXPeyuh2mv2_hKIlMgSyffIxZ8jgrftXgvlkrwxNzF6zRNs32IzBgJquo7p6L1Kg7P4h7vnlRaWjR3PwBKnDij6xoraLxCKnaaVAu-IpIjRDxmyBov0SWh4voyNVqE9_92qRIKOsYyQKh63hlBxyyu58sXwCemBoTKPLR-Qm2s09XJYAo2fqL8moYBXCJB9u2-',
                'box_color': 'Velvet Plum',
                'rating': Decimal('5.0'),
                'reviews_count': 96,
                'is_featured': True,
                'is_bestseller': False,
            },
        ]

        for p in products_data:
            obj, created = Product.objects.update_or_create(
                slug=p['slug'],
                defaults=p
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status} Product: {obj.name} (PKR {obj.price})")

        # 5. Create default Superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@tinytreasure.pk',
                password='adminpassword123'
            )
            Customer.objects.get_or_create(
                user=admin_user,
                defaults={
                    'full_name': 'Atelier Administrator',
                    'email': 'admin@tinytreasure.pk',
                    'phone': '03001234567',
                    'city': 'Islamabad'
                }
            )
            self.stdout.write(self.style.SUCCESS("  Created default admin user: 'admin' with password: 'adminpassword123'"))
        else:
            self.stdout.write("  Admin user already exists.")

        self.stdout.write(self.style.SUCCESS("Successfully seeded Tiny Treasure Co. database!"))
