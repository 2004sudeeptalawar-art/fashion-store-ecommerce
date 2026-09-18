import random
from models import db, User, Category, Product, ProductVariant, Review, Address

def seed_database():
    """Seed the database with rich categories, products, variants, and reviews."""
    if Category.query.first():
        print("Database already seeded.")
        return

    print("Seeding database with luxury fashion catalog...")

    # 1. Create Default Users (Admin & Customer)
    admin_user = User(
        full_name="Alexander Vance (Admin)",
        email="admin@vogue.com",
        phone="+91 98765 43210",
        is_admin=True,
        avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80"
    )
    admin_user.set_password("admin123")

    customer_user = User(
        full_name="Sophia Laurent",
        email="sophia@example.com",
        phone="+91 98989 12345",
        is_admin=False,
        avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"
    )
    customer_user.set_password("user123")

    db.session.add(admin_user)
    db.session.add(customer_user)
    db.session.flush()

    # Add default address for demo customer
    default_address = Address(
        user_id=customer_user.id,
        full_name="Sophia Laurent",
        phone="+91 98989 12345",
        address_line="Flat 402, Royale Heights, MG Road",
        landmark="Near Central Boulevard",
        city="Mumbai",
        state="Maharashtra",
        pincode="400001",
        is_default=True,
        address_type="Home"
    )
    db.session.add(default_address)

    # 2. Create Luxury Categories
    categories_data = [
        {
            "name": "Women's Collection",
            "slug": "womens-collection",
            "desc": "Timeless silhouettes, evening dresses, structured blazers, and artisanal silk pieces.",
            "img": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
            "order": 1
        },
        {
            "name": "Men's Tailoring",
            "slug": "mens-tailoring",
            "desc": "Italian tailored suits, relaxed linen shirts, cashmere knits, and contemporary streetwear.",
            "img": "https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?auto=format&fit=crop&w=800&q=80",
            "order": 2
        },
        {
            "name": "Luxury Accessories",
            "slug": "luxury-accessories",
            "desc": "Handcrafted leather totes, minimalist sunglasses, gold-accented belts, and silk scarves.",
            "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80",
            "order": 3
        },
        {
            "name": "Designer Footwear",
            "slug": "designer-footwear",
            "desc": "Sculpted leather boots, bespoke oxfords, luxury minimalist sneakers, and statement heels.",
            "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80",
            "order": 4
        },
        {
            "name": "Haute Joaillerie",
            "slug": "haute-joaillerie",
            "desc": "Refined 18k gold vermeil, bezel-set cubic zirconia, and bespoke timeless jewelry.",
            "img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
            "order": 5
        }
    ]

    cat_map = {}
    for c in categories_data:
        cat = Category(
            category_name=c["name"],
            slug=c["slug"],
            description=c["desc"],
            image_url=c["img"],
            display_order=c["order"]
        )
        db.session.add(cat)
        cat_map[c["slug"]] = cat

    db.session.flush()

    # 3. Create Curated Products with Variants & Reviews
    products_data = [
        # Women
        {
            "cat_slug": "womens-collection",
            "name": "L'Étoile Velvet Evening Gown",
            "slug": "letoile-velvet-evening-gown",
            "subtitle": "Couture Midnight Draped Silhouette",
            "description": "Crafted from sumptuous micro-velvet, the L'Étoile gown features an asymmetrical sculpted neckline and a daring thigh-high slit. Designed for black-tie galas and unforgettable evenings.",
            "material": "92% Italian Silk Velvet, 8% Elastane",
            "care": "Professional Dry Clean Only",
            "base_price": 4999.00,
            "original_price": 6499.00,
            "discount": 23,
            "badge": "BESTSELLER",
            "is_featured": True,
            "rating": 4.9,
            "reviews_count": 28,
            "img": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "XS", "color": "Midnight Black", "hex": "#111111", "price": 4999.00, "stock": 8},
                {"size": "S", "color": "Midnight Black", "hex": "#111111", "price": 4999.00, "stock": 15},
                {"size": "M", "color": "Midnight Black", "hex": "#111111", "price": 4999.00, "stock": 12},
                {"size": "L", "color": "Midnight Black", "hex": "#111111", "price": 4999.00, "stock": 6},
                {"size": "S", "color": "Royal Emerald", "hex": "#0a4d3c", "price": 5299.00, "stock": 10},
                {"size": "M", "color": "Royal Emerald", "hex": "#0a4d3c", "price": 5299.00, "stock": 14},
            ],
            "reviews": [
                {"user": "Claire D.", "rating": 5, "title": "Absolute showstopper!", "comment": "Wore this to a charity gala and received endless compliments. The drape is breathtaking."},
                {"user": "Evelyn K.", "rating": 5, "title": "Flawless fit and quality", "comment": "The velvet is heavy and expensive-feeling. Fits like a glove."}
            ]
        },
        {
            "cat_slug": "womens-collection",
            "name": "Oversized Cashmere Boyfriend Trench",
            "slug": "oversized-cashmere-boyfriend-trench",
            "subtitle": "Double-Breasted Parisian Outerwear",
            "description": "An essential layering masterpiece. Spun from pure Mongolian cashmere with horn button fastenings, wide storm flaps, and a relaxed dropped-shoulder cut.",
            "material": "100% Grade-A Mongolian Cashmere",
            "care": "Specialist Wool Clean Only",
            "base_price": 6899.00,
            "original_price": 8999.00,
            "discount": 23,
            "badge": "TRENDING",
            "is_featured": True,
            "rating": 4.8,
            "reviews_count": 19,
            "img": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "S", "color": "Warm Camel", "hex": "#c19a6b", "price": 6899.00, "stock": 10},
                {"size": "M", "color": "Warm Camel", "hex": "#c19a6b", "price": 6899.00, "stock": 12},
                {"size": "L", "color": "Warm Camel", "hex": "#c19a6b", "price": 6899.00, "stock": 5},
                {"size": "S", "color": "Oatmeal Beige", "hex": "#d8cca3", "price": 6899.00, "stock": 8},
                {"size": "M", "color": "Oatmeal Beige", "hex": "#d8cca3", "price": 6899.00, "stock": 9},
            ],
            "reviews": [
                {"user": "Valerie S.", "rating": 5, "title": "So warm and chic", "comment": "My go-to trench for autumn and winter travel. Utterly luxurious."}
            ]
        },
        {
            "cat_slug": "womens-collection",
            "name": "Aura Mulberry Silk Slip Dress",
            "slug": "aura-mulberry-silk-slip-dress",
            "subtitle": "Bias-Cut 22-Momme Pure Silk",
            "description": "Fluid, luminous, and gracefully draped across the collarbones. Wear it standalone with strappy heels or styled over a fine-knit turtleneck.",
            "material": "100% 22-Momme Mulberry Silk",
            "care": "Hand Wash Cold or Dry Clean",
            "base_price": 3299.00,
            "original_price": 4200.00,
            "discount": 21,
            "badge": "NEW",
            "is_featured": False,
            "rating": 4.7,
            "reviews_count": 14,
            "img": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "XS", "color": "Champagne Rose", "hex": "#e7c9c0", "price": 3299.00, "stock": 7},
                {"size": "S", "color": "Champagne Rose", "hex": "#e7c9c0", "price": 3299.00, "stock": 14},
                {"size": "M", "color": "Champagne Rose", "hex": "#e7c9c0", "price": 3299.00, "stock": 11},
                {"size": "S", "color": "Onyx Black", "hex": "#1a1a1a", "price": 3299.00, "stock": 10},
                {"size": "M", "color": "Onyx Black", "hex": "#1a1a1a", "price": 3299.00, "stock": 15},
            ],
            "reviews": [
                {"user": "Maya R.", "rating": 5, "title": "Feels like a second skin", "comment": "The silk is extraordinarily soft and has that subtle pearlescent sheen."}
            ]
        },

        # Men
        {
            "cat_slug": "mens-tailoring",
            "name": "Savile Structured Wool Tuxedo",
            "slug": "savile-structured-wool-tuxedo",
            "subtitle": "Satin Peak Lapel Slim-Fit Two-Piece",
            "description": "Tailored from Super 140s virgin wool with glossy silk satin lapels and hand-finished pick stitching. Engineered to deliver effortless authority and poise.",
            "material": "100% Super 140s Italian Virgin Wool",
            "care": "Specialist Dry Clean Only",
            "base_price": 7999.00,
            "original_price": 10500.00,
            "discount": 24,
            "badge": "LUXE",
            "is_featured": True,
            "rating": 5.0,
            "reviews_count": 31,
            "img": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "38R", "color": "Midnight Tuxedo Black", "hex": "#0a0a0a", "price": 7999.00, "stock": 5},
                {"size": "40R", "color": "Midnight Tuxedo Black", "hex": "#0a0a0a", "price": 7999.00, "stock": 8},
                {"size": "42R", "color": "Midnight Tuxedo Black", "hex": "#0a0a0a", "price": 7999.00, "stock": 7},
                {"size": "40R", "color": "Deep Navy Blue", "hex": "#0d1b2a", "price": 7999.00, "stock": 6},
                {"size": "42R", "color": "Deep Navy Blue", "hex": "#0d1b2a", "price": 7999.00, "stock": 4},
            ],
            "reviews": [
                {"user": "Marcus B.", "rating": 5, "title": "Bespoke level craftsmanship", "comment": "Impeccable shoulder construction and fit. Looked unmatched at my wedding."}
            ]
        },
        {
            "cat_slug": "mens-tailoring",
            "name": "Riviera Relaxed Linen Resort Shirt",
            "slug": "riviera-relaxed-linen-resort-shirt",
            "subtitle": "Camp Collar French Flax Shirt",
            "description": "Breathable 100% Normandy linen washed for supreme softness. Features genuine mother-of-pearl buttons and a laid-back Cuban collar silhouette.",
            "material": "100% Normandy Linen",
            "care": "Machine Wash Cold, Hang Dry",
            "base_price": 2499.00,
            "original_price": 3199.00,
            "discount": 22,
            "badge": "NEW",
            "is_featured": False,
            "rating": 4.6,
            "reviews_count": 22,
            "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "S", "color": "Crisp White", "hex": "#fcfcfc", "price": 2499.00, "stock": 14},
                {"size": "M", "color": "Crisp White", "hex": "#fcfcfc", "price": 2499.00, "stock": 20},
                {"size": "L", "color": "Crisp White", "hex": "#fcfcfc", "price": 2499.00, "stock": 15},
                {"size": "M", "color": "Sage Green", "hex": "#879f84", "price": 2499.00, "stock": 12},
                {"size": "L", "color": "Sage Green", "hex": "#879f84", "price": 2499.00, "stock": 9},
            ],
            "reviews": [
                {"user": "Julian P.", "rating": 5, "title": "Cool and comfortable", "comment": "Essential for summer vacations. Fabric doesn't itch at all."}
            ]
        },
        {
            "cat_slug": "mens-tailoring",
            "name": "Milano Heavyweight Merino Knit Sweater",
            "slug": "milano-heavyweight-merino-knit-sweater",
            "subtitle": "Chunky Waffle Texture Crewneck",
            "description": "Crafted from extra-fine 19.5-micron Merino wool. Thermoregulating, ultra-durable, and finished with ribbed trims for a snug yet relaxed drape.",
            "material": "100% Extra-fine Merino Wool",
            "care": "Hand Wash Cold / Flat Dry",
            "base_price": 3899.00,
            "original_price": 4899.00,
            "discount": 20,
            "badge": "BESTSELLER",
            "is_featured": True,
            "rating": 4.9,
            "reviews_count": 27,
            "img": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "S", "color": "Charcoal Grey", "hex": "#36454f", "price": 3899.00, "stock": 9},
                {"size": "M", "color": "Charcoal Grey", "hex": "#36454f", "price": 3899.00, "stock": 16},
                {"size": "L", "color": "Charcoal Grey", "hex": "#36454f", "price": 3899.00, "stock": 11},
                {"size": "M", "color": "Alabaster Cream", "hex": "#f5f2eb", "price": 3899.00, "stock": 14},
                {"size": "L", "color": "Alabaster Cream", "hex": "#f5f2eb", "price": 3899.00, "stock": 8},
            ],
            "reviews": [
                {"user": "David T.", "rating": 5, "title": "Perfection", "comment": "Substantial weight without feeling bulky. Keeps you wonderfully warm."}
            ]
        },

        # Accessories
        {
            "cat_slug": "luxury-accessories",
            "name": "Palermo Full-Grain Leather Satchel",
            "slug": "palermo-full-grain-leather-satchel",
            "subtitle": "Vegetable-Tanned Tuscan Calfskin",
            "description": "Hand-stitched in Florence with burnished edges and solid brass hardware. Fits up to a 16-inch laptop with multiple dedicated internal organizers.",
            "material": "100% Tuscan Full-Grain Vegetable-Tanned Leather",
            "care": "Treat with Natural Leather Balm",
            "base_price": 5499.00,
            "original_price": 6999.00,
            "discount": 21,
            "badge": "LUXE",
            "is_featured": True,
            "rating": 4.9,
            "reviews_count": 35,
            "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "Standard", "color": "Espresso Cognac", "hex": "#4a2c11", "price": 5499.00, "stock": 12},
                {"size": "Standard", "color": "Carbon Black", "hex": "#111111", "price": 5499.00, "stock": 18},
            ],
            "reviews": [
                {"user": "Gregory L.", "rating": 5, "title": "Patina develops beautifully", "comment": "6 months of daily use and the leather looks richer with each passing week."}
            ]
        },
        {
            "cat_slug": "luxury-accessories",
            "name": "Aviateur Gold-Trimmed Sunglasses",
            "slug": "aviateur-gold-trimmed-sunglasses",
            "subtitle": "Handmade Acetate & Titanium Frame",
            "description": "Japanese titanium hardware with polarized UV400 anti-reflective lenses. Lightweight ergonomic bridge with bespoke monogram temples.",
            "material": "Mazzucchelli Acetate & Japanese Titanium",
            "care": "Clean with Included Microfiber Cloth",
            "base_price": 1899.00,
            "original_price": 2500.00,
            "discount": 24,
            "badge": "TRENDING",
            "is_featured": False,
            "rating": 4.7,
            "reviews_count": 18,
            "img": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "Free Size", "color": "Havana Gold / Amber", "hex": "#784b24", "price": 1899.00, "stock": 25},
                {"size": "Free Size", "color": "Obsidian / Gradient Grey", "hex": "#1c1c1c", "price": 1899.00, "stock": 20},
            ],
            "reviews": [
                {"user": "Samantha W.", "rating": 5, "title": "Iconic look", "comment": "Subtle luxury and great sun protection. Does not pinch the nose."}
            ]
        },

        # Footwear
        {
            "cat_slug": "designer-footwear",
            "name": "Verona Handcrafted Chelsea Boots",
            "slug": "verona-handcrafted-chelsea-boots",
            "subtitle": "Goodyear-Welted Italian Box Calf Leather",
            "description": "A refined modern profile featuring double elasticated side gussets, studded rubber Vibram half-soles, and hand-stained burnished toe caps.",
            "material": "100% French Calfskin Leather, Goodyear Welted",
            "care": "Wax Polish and Cedar Shoe Trees",
            "base_price": 6299.00,
            "original_price": 7999.00,
            "discount": 21,
            "badge": "BESTSELLER",
            "is_featured": True,
            "rating": 4.9,
            "reviews_count": 42,
            "img": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "UK 7 / EU 41", "color": "Mahogany Brown", "hex": "#3d1f14", "price": 6299.00, "stock": 6},
                {"size": "UK 8 / EU 42", "color": "Mahogany Brown", "hex": "#3d1f14", "price": 6299.00, "stock": 10},
                {"size": "UK 9 / EU 43", "color": "Mahogany Brown", "hex": "#3d1f14", "price": 6299.00, "stock": 8},
                {"size": "UK 8 / EU 42", "color": "Midnight Black", "hex": "#0d0d0d", "price": 6299.00, "stock": 9},
                {"size": "UK 9 / EU 43", "color": "Midnight Black", "hex": "#0d0d0d", "price": 6299.00, "stock": 7},
            ],
            "reviews": [
                {"user": "Nathan R.", "rating": 5, "title": "Worth every single rupee", "comment": "The Goodyear welt construction is top tier. Broke in comfortably in just 2 days."}
            ]
        },
        {
            "cat_slug": "designer-footwear",
            "name": "Monolith Chunky Leather Loafers",
            "slug": "monolith-chunky-leather-loafers",
            "subtitle": "Brushed Leather Penny Loafer with Lug Sole",
            "description": "Bold runway-inspired silhouette with exaggerated cleated tread soles and a signature enamel triangle crest strap.",
            "material": "Brushed Glazed Calfskin Leather",
            "care": "Wipe with damp cloth and leather cream",
            "base_price": 5799.00,
            "original_price": 7200.00,
            "discount": 19,
            "badge": "TRENDING",
            "is_featured": False,
            "rating": 4.8,
            "reviews_count": 16,
            "img": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "UK 6 / EU 39", "color": "Glazed Jet Black", "hex": "#050505", "price": 5799.00, "stock": 5},
                {"size": "UK 7 / EU 40", "color": "Glazed Jet Black", "hex": "#050505", "price": 5799.00, "stock": 8},
                {"size": "UK 8 / EU 41", "color": "Glazed Jet Black", "hex": "#050505", "price": 5799.00, "stock": 6},
            ],
            "reviews": [
                {"user": "Helena V.", "rating": 5, "title": "Stunning statement shoe", "comment": "Super stylish and adds great height while remaining very comfortable."}
            ]
        },

        # Jewelry
        {
            "cat_slug": "haute-joaillerie",
            "name": "Soleil 18K Gold Vermeil Choker",
            "slug": "soleil-18k-gold-vermeil-choker",
            "subtitle": "Micro-Pavé Radiant Sunbeam Collar",
            "description": "Crafted in heavy 2.5-micron 18-karat yellow gold over recycled sterling silver with conflict-free hand-set stones.",
            "material": "18k Yellow Gold Vermeil (Sterling Silver 925 Core)",
            "care": "Store in Anti-Tarnish Pouch, Avoid Water",
            "base_price": 2899.00,
            "original_price": 3699.00,
            "discount": 21,
            "badge": "NEW",
            "is_featured": True,
            "rating": 4.9,
            "reviews_count": 25,
            "img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
            "extras": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=80",
            "variants": [
                {"size": "Adjustable (38-45cm)", "color": "18K Yellow Gold", "hex": "#d4af37", "price": 2899.00, "stock": 18},
                {"size": "Adjustable (38-45cm)", "color": "Platinum Rhodium", "hex": "#e5e4e2", "price": 2899.00, "stock": 12},
            ],
            "reviews": [
                {"user": "Isabella N.", "rating": 5, "title": "Pure elegance", "comment": "Dainty yet makes such a sparkling statement. Beautifully packaged in a velvet box."}
            ]
        }
    ]

    for p_data in products_data:
        cat = cat_map[p_data["cat_slug"]]
        product = Product(
            category_id=cat.category_id,
            product_name=p_data["name"],
            slug=p_data["slug"],
            subtitle=p_data["subtitle"],
            description=p_data["description"],
            material_info=p_data["material"],
            care_instructions=p_data["care"],
            base_price=p_data["base_price"],
            original_price=p_data["original_price"],
            discount_percent=p_data["discount"],
            badge=p_data["badge"],
            is_featured=p_data["is_featured"],
            rating=p_data["rating"],
            reviews_count=p_data["reviews_count"],
            image_url=p_data["img"],
            additional_images=p_data["extras"]
        )
        db.session.add(product)
        db.session.flush()

        # Add variants
        for v in p_data["variants"]:
            variant = ProductVariant(
                product_id=product.product_id,
                size_label=v["size"],
                color=v["color"],
                color_hex=v.get("hex", "#111111"),
                sku=f"SKU-{product.product_id}-{v['size']}-{v['color'][:3].upper()}",
                price=v["price"],
                stock_quantity=v["stock"],
                is_available=True
            )
            db.session.add(variant)

        # Add reviews
        for r in p_data.get("reviews", []):
            review = Review(
                product_id=product.product_id,
                user_id=customer_user.id,
                user_name=r["user"],
                rating=r["rating"],
                headline=r["title"],
                comment=r["comment"],
                verified_purchase=True
            )
            db.session.add(review)

    db.session.commit()
    print(f"Successfully seeded database with {len(categories_data)} categories and {len(products_data)} luxury products!")
