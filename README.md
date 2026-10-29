# Tiny Treasure Co. (The Gift Edit) - Django E-Commerce Backend

A luxury bespoke e-commerce store developed with **Python and Django**, integrating the existing frontend design system without altering its delicate aesthetic, typography, or responsive layout.

---

## 🌟 Key Features Implemented

1. **Dynamic Database Catalog:**
   - Database-backed categories, products, box finishes, and atelier items in SQLite.
   - Dynamic product cards, pricing in PKR, badges, star ratings, and item inclusion pills.

2. **Interactive 5-Step Atelier Box Customizer:**
   - Occasion selector (Birthday, Best Friend, Anniversary, Graduation, Self-Care).
   - Keepsake box presentation finish selector (Blush Silk, Warm Cream, Sage Botanical, Velvet Plum).
   - Base curation format / tiers (Mini Delight, Classic Edit, Luxury Keepsake).
   - Add-on artisanal gift items checklist with live image previews and prices.
   - Deckle-edge calligraphy card customization with real-time text and wax seal preview.
   - Server-side verified price calculation preventing client-side tampering.

3. **Persistent Shopping Cart:**
   - Supports both curated catalog boxes and bespoke custom-built boxes.
   - Add to cart with personalized handwritten calligraphy message and wax seal color preference.
   - AJAX quantity update (+ / -) and item removal with instant recalculation.
   - Dynamic cart badge and subtotal updates across all pages.
   - Session-backed persistence for guests with automatic transfer upon account login.

4. **Pakistan-Tailored Checkout & Orders:**
   - Sender information, surprise gifting toggle (hides receipts and invoices for recipients).
   - Full recipient address with city selection (Islamabad, Rawalpindi, Lahore, Karachi, etc.).
   - Cash on Delivery (COD) as primary payment method.
   - Direct Bank Transfer / Raast Instant Pay with bank account details (Meezan Bank, IBAN, Raast ID).
   - Credit / Debit card simulation.
   - Server-side total calculation: Free express courier delivery on orders PKR 3,000+ (PKR 250 standard courier fee otherwise).
   - Unique order numbers generated automatically (e.g., `TGE-PK-8924`).

5. **Customer Authentication & Profiles:**
   - Registration with full name, email, Pakistani phone number, and password validation.
   - Login via username or email address.
   - Customer profile dashboard displaying order history, status, and itemized receipts.

6. **Contact Concierge & Newsletter:**
   - Contact form with database persistence in `ContactMessage`.
   - Atelier Circle VIP newsletter subscription saved to `NewsletterSubscriber`.

7. **Django Admin Panel:**
   - Complete management for Products, Categories, Box Finishes, Atelier Items, Customers, Orders, Order Items, and Contact Inquiries.
   - Search, filters, inline order items, and status updates (`received`, `handcrafting`, `dispatched`, `delivered`).

---

## 📁 Project Structure

```
stitch_tiny_treasure_co._e_commerce_store/
├── db.sqlite3                      # SQLite development database
├── manage.py                       # Django CLI management entrypoint
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation & commands
├── tinytreasure/                   # Core Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Settings, apps, templates, static/media
│   ├── urls.py                     # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── store/                          # Main e-commerce application
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py
│   ├── context_processors.py       # Global cart and category state
│   ├── forms.py                    # Registration, Login, Checkout, Contact forms
│   ├── models.py                   # Category, Product, Cart, Order, Customer, etc.
│   ├── tests.py                    # Comprehensive automated test suite
│   ├── urls.py                     # App URL routing
│   ├── views.py                    # Controllers and business logic
│   └── management/commands/
│       └── seed_data.py            # Initial catalog and admin seeder
├── templates/                      # Django HTML templates
│   ├── base.html                   # Master layout with matching Tailwind & fonts
│   ├── store/
│   │   ├── home.html               # Boutique homepage
│   │   ├── shop.html               # Catalog with category, price, search filters
│   │   ├── customize.html          # 5-step atelier box builder
│   │   ├── cart_checkout.html      # Integrated cart review & checkout
│   │   ├── order_confirmation.html # Order receipt & WhatsApp tracking
│   │   ├── contact.html            # Contact concierge form
│   │   └── about.html              # Atelier philosophy & story
│   └── accounts/
│       ├── login.html              # Customer login
│       ├── register.html           # Customer registration
│       └── profile.html            # Profile & order history
├── static/                         # Static assets (images, css, js)
│   └── images/
└── media/                          # Uploaded product imagery
```

---

## 🚀 Windows Setup & Running Instructions

Open PowerShell or Command Prompt in the project folder:

```powershell
cd "c:\Users\Khazima\Downloads\stitch_tiny_treasure_co._e_commerce_store"
```

### 1. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 2. Run Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Initial Products & Create Admin Account
```powershell
python manage.py seed_data
```
*This command seeds all 6 signature gift boxes, 5 occasion categories, 4 keepsake box finishes, 7 atelier items, and creates a default superuser.*

Default Administrator Credentials:
- **Username:** `admin`
- **Admin Panel URL:** `http://127.0.0.1:8000/admin/`

### 4. Run Automated Test Suite
```powershell
python manage.py test store
```

### 5. Start the Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```

Access the store in your browser:
- **Homepage:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Shop Catalog:** [http://127.0.0.1:8000/shop/](http://127.0.0.1:8000/shop/)
- **Customize Box:** [http://127.0.0.1:8000/customize/](http://127.0.0.1:8000/customize/)
- **Cart & Checkout:** [http://127.0.0.1:8000/checkout/](http://127.0.0.1:8000/checkout/)
- **Contact:** [http://127.0.0.1:8000/contact/](http://127.0.0.1:8000/contact/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
