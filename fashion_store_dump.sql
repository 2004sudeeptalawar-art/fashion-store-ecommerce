-- ========================================================================
-- ATELIER & CO. | FASHION STORE MYSQL DATABASE DUMP & SEED SCRIPT
-- Import this file in MySQL Workbench, phpMyAdmin, DBeaver, or mysql CLI:
-- mysql -u root -p < fashion_store_dump.sql
-- ========================================================================

CREATE DATABASE IF NOT EXISTS `fashion_store` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `fashion_store`;

-- 1. Users Table
DROP TABLE IF EXISTS `wishlist`;
DROP TABLE IF EXISTS `reviews`;
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `addresses`;
DROP TABLE IF EXISTS `cart_items`;
DROP TABLE IF EXISTS `cart`;
DROP TABLE IF EXISTS `product_variants`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `full_name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(150) NOT NULL UNIQUE,
  `phone` VARCHAR(20) NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `is_admin` BOOLEAN DEFAULT FALSE,
  `avatar_url` VARCHAR(255) DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Categories Table
CREATE TABLE `categories` (
  `category_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_name` VARCHAR(100) NOT NULL UNIQUE,
  `slug` VARCHAR(120) NOT NULL UNIQUE,
  `description` TEXT NULL,
  `image_url` VARCHAR(500) NULL,
  `is_active` BOOLEAN DEFAULT TRUE,
  `display_order` INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Products Table
CREATE TABLE `products` (
  `product_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_id` INT NOT NULL,
  `product_name` VARCHAR(200) NOT NULL,
  `slug` VARCHAR(220) NOT NULL UNIQUE,
  `subtitle` VARCHAR(255) DEFAULT 'Exclusive Designer Collection',
  `description` TEXT NOT NULL,
  `material_info` VARCHAR(255) DEFAULT '100% Premium Pure Cotton / Sustainable Blend',
  `care_instructions` VARCHAR(255) DEFAULT 'Dry Clean Only / Gentle Machine Wash',
  `base_price` FLOAT NOT NULL,
  `original_price` FLOAT NULL,
  `discount_percent` INT DEFAULT 0,
  `image_url` VARCHAR(500) NOT NULL,
  `additional_images` TEXT NULL,
  `badge` VARCHAR(50) DEFAULT 'NEW',
  `is_featured` BOOLEAN DEFAULT FALSE,
  `is_active` BOOLEAN DEFAULT TRUE,
  `rating` FLOAT DEFAULT 4.8,
  `reviews_count` INT DEFAULT 12,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Product Variants Table
CREATE TABLE `product_variants` (
  `variant_id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_id` INT NOT NULL,
  `size_label` VARCHAR(30) NOT NULL,
  `color` VARCHAR(50) NOT NULL,
  `color_hex` VARCHAR(20) DEFAULT '#1a1a1a',
  `sku` VARCHAR(100) UNIQUE NULL,
  `price` FLOAT NOT NULL,
  `stock_quantity` INT DEFAULT 15,
  `is_available` BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Addresses Table
CREATE TABLE `addresses` (
  `address_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `full_name` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `address_line` VARCHAR(255) NOT NULL,
  `landmark` VARCHAR(150) NULL,
  `city` VARCHAR(100) NOT NULL,
  `state` VARCHAR(100) NOT NULL,
  `pincode` VARCHAR(20) NOT NULL,
  `is_default` BOOLEAN DEFAULT FALSE,
  `address_type` VARCHAR(20) DEFAULT 'Home',
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Orders Table
CREATE TABLE `orders` (
  `order_id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_number` VARCHAR(50) NOT NULL UNIQUE,
  `user_id` INT NOT NULL,
  `address_id` INT NULL,
  `address_snapshot` TEXT NULL,
  `subtotal` FLOAT NOT NULL,
  `tax_amount` FLOAT DEFAULT 0.0,
  `delivery_charge` FLOAT DEFAULT 0.0,
  `discount_amount` FLOAT DEFAULT 0.0,
  `total_amount` FLOAT NOT NULL,
  `payment_method` VARCHAR(50) DEFAULT 'Cash on Delivery',
  `payment_status` VARCHAR(50) DEFAULT 'Pending',
  `order_status` VARCHAR(50) DEFAULT 'Order Placed',
  `tracking_number` VARCHAR(100) NULL,
  `order_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Order Items Table
CREATE TABLE `order_items` (
  `order_item_id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `variant_id` INT NULL,
  `product_id` INT NULL,
  `product_name` VARCHAR(200) NOT NULL,
  `size_label` VARCHAR(30) NULL,
  `color` VARCHAR(50) NULL,
  `image_url` VARCHAR(500) NULL,
  `unit_price` FLOAT NOT NULL,
  `quantity` INT NOT NULL,
  `subtotal` FLOAT NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Cart and Cart Items
CREATE TABLE `cart` (
  `cart_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `session_token` VARCHAR(100) NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cart_items` (
  `cart_item_id` INT AUTO_INCREMENT PRIMARY KEY,
  `cart_id` INT NOT NULL,
  `variant_id` INT NOT NULL,
  `quantity` INT DEFAULT 1,
  `unit_price` FLOAT NOT NULL,
  FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE CASCADE,
  FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`variant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Reviews Table
CREATE TABLE `reviews` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_id` INT NOT NULL,
  `user_id` INT NULL,
  `user_name` VARCHAR(100) NOT NULL,
  `rating` INT DEFAULT 5,
  `headline` VARCHAR(150) NULL,
  `comment` TEXT NOT NULL,
  `verified_purchase` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Wishlist Table
CREATE TABLE `wishlist` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_user_product_wishlist` (`user_id`, `product_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================================================================
-- SEED DATA INSERTIONS
-- ========================================================================

-- Users (admin123 & user123)
INSERT INTO `users` (`id`, `full_name`, `email`, `phone`, `password_hash`, `is_admin`, `avatar_url`) VALUES
(1, 'Alexander Vance (Admin)', 'admin@vogue.com', '+91 98765 43210', 'scrypt:32768:8:1$uH39r4oB1nJd$2a40608f0a071fe39b03ae285ee19ae8757041a8faeb783ffc977d4410a7f76ca6c18be3ce5b10fcb9c8c5c7d8102d40905477c7b82772ca417ff62ecbbfbe77', 1, 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80'),
(2, 'Sophia Laurent', 'sophia@example.com', '+91 98989 12345', 'scrypt:32768:8:1$uH39r4oB1nJd$2a40608f0a071fe39b03ae285ee19ae8757041a8faeb783ffc977d4410a7f76ca6c18be3ce5b10fcb9c8c5c7d8102d40905477c7b82772ca417ff62ecbbfbe77', 0, 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80');

-- Categories
INSERT INTO `categories` (`category_id`, `category_name`, `slug`, `description`, `image_url`, `is_active`, `display_order`) VALUES
(1, 'Women\'s Collection', 'womens-collection', 'Timeless silhouettes, evening dresses, structured blazers, and artisanal silk pieces.', 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80', 1, 1),
(2, 'Men\'s Tailoring', 'mens-tailoring', 'Italian tailored suits, relaxed linen shirts, cashmere knits, and contemporary streetwear.', 'https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?auto=format&fit=crop&w=800&q=80', 1, 2),
(3, 'Luxury Accessories', 'luxury-accessories', 'Handcrafted leather totes, minimalist sunglasses, gold-accented belts, and silk scarves.', 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80', 1, 3),
(4, 'Designer Footwear', 'designer-footwear', 'Sculpted leather boots, bespoke oxfords, luxury minimalist sneakers, and statement heels.', 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80', 1, 4),
(5, 'Haute Joaillerie', 'haute-joaillerie', 'Refined 18k gold vermeil, bezel-set cubic zirconia, and bespoke timeless jewelry.', 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80', 1, 5);

-- Products
INSERT INTO `products` (`product_id`, `category_id`, `product_name`, `slug`, `subtitle`, `description`, `material_info`, `care_instructions`, `base_price`, `original_price`, `discount_percent`, `image_url`, `additional_images`, `badge`, `is_featured`, `is_active`, `rating`, `reviews_count`) VALUES
(1, 1, 'L\'Étoile Velvet Evening Gown', 'letoile-velvet-evening-gown', 'Couture Midnight Draped Silhouette', 'Crafted from sumptuous micro-velvet, the L\'Étoile gown features an asymmetrical sculpted neckline and a daring thigh-high slit.', '92% Italian Silk Velvet, 8% Elastane', 'Professional Dry Clean Only', 4999.00, 6499.00, 23, 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=80', 'BESTSELLER', 1, 1, 4.9, 28),
(2, 1, 'Oversized Cashmere Boyfriend Trench', 'oversized-cashmere-boyfriend-trench', 'Double-Breasted Parisian Outerwear', 'An essential layering masterpiece. Spun from pure Mongolian cashmere with horn button fastenings and wide storm flaps.', '100% Grade-A Mongolian Cashmere', 'Specialist Wool Clean Only', 6899.00, 8999.00, 23, 'https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=80', 'TRENDING', 1, 1, 4.8, 19),
(3, 1, 'Aura Mulberry Silk Slip Dress', 'aura-mulberry-silk-slip-dress', 'Bias-Cut 22-Momme Pure Silk', 'Fluid, luminous, and gracefully draped across the collarbones. Wear it standalone or styled over fine knitwear.', '100% 22-Momme Mulberry Silk', 'Hand Wash Cold or Dry Clean', 3299.00, 4200.00, 21, 'https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?auto=format&fit=crop&w=800&q=80', 'NEW', 0, 1, 4.7, 14),
(4, 2, 'Savile Structured Wool Tuxedo', 'savile-structured-wool-tuxedo', 'Satin Peak Lapel Slim-Fit Two-Piece', 'Tailored from Super 140s virgin wool with glossy silk satin lapels and hand-finished pick stitching.', '100% Super 140s Italian Virgin Wool', 'Specialist Dry Clean Only', 7999.00, 10500.00, 24, 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80', 'LUXE', 1, 1, 5.0, 31),
(5, 2, 'Riviera Relaxed Linen Resort Shirt', 'riviera-relaxed-linen-resort-shirt', 'Camp Collar French Flax Shirt', 'Breathable 100% Normandy linen washed for supreme softness with genuine mother-of-pearl buttons.', '100% Normandy Linen', 'Machine Wash Cold, Hang Dry', 2499.00, 3199.00, 22, 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80', 'NEW', 0, 1, 4.6, 22),
(6, 2, 'Milano Heavyweight Merino Knit Sweater', 'milano-heavyweight-merino-knit-sweater', 'Chunky Waffle Texture Crewneck', 'Crafted from extra-fine 19.5-micron Merino wool. Thermoregulating, ultra-durable, with ribbed trims.', '100% Extra-fine Merino Wool', 'Hand Wash Cold / Flat Dry', 3899.00, 4899.00, 20, 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?auto=format&fit=crop&w=800&q=80', 'BESTSELLER', 1, 1, 4.9, 27),
(7, 3, 'Palermo Full-Grain Leather Satchel', 'palermo-full-grain-leather-satchel', 'Vegetable-Tanned Tuscan Calfskin', 'Hand-stitched in Florence with burnished edges and solid brass hardware. Fits a 16-inch laptop.', '100% Tuscan Full-Grain Vegetable-Tanned Leather', 'Treat with Natural Leather Balm', 5499.00, 6999.00, 21, 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80', 'LUXE', 1, 1, 4.9, 35),
(8, 3, 'Aviateur Gold-Trimmed Sunglasses', 'aviateur-gold-trimmed-sunglasses', 'Handmade Acetate & Titanium Frame', 'Japanese titanium hardware with polarized UV400 anti-reflective lenses and ergonomic bridge.', 'Mazzucchelli Acetate & Japanese Titanium', 'Clean with Microfiber Cloth', 1899.00, 2500.00, 24, 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=800&q=80', 'TRENDING', 0, 1, 4.7, 18),
(9, 4, 'Verona Handcrafted Chelsea Boots', 'verona-handcrafted-chelsea-boots', 'Goodyear-Welted Italian Box Calf Leather', 'Double elasticated gussets, studded rubber Vibram half-soles, and hand-stained burnished toe caps.', '100% French Calfskin Leather, Goodyear Welted', 'Wax Polish and Cedar Shoe Trees', 6299.00, 7999.00, 21, 'https://images.unsplash.com/photo-1638247025967-b4e38f787b76?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80', 'BESTSELLER', 1, 1, 4.9, 42),
(10, 4, 'Monolith Chunky Leather Loafers', 'monolith-chunky-leather-loafers', 'Brushed Leather Penny Loafer with Lug Sole', 'Exaggerated cleated tread soles with signature enamel crest strap.', 'Brushed Glazed Calfskin Leather', 'Wipe with damp cloth and leather cream', 5799.00, 7200.00, 19, 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=800&q=80', 'TRENDING', 0, 1, 4.8, 16),
(11, 5, 'Soleil 18K Gold Vermeil Choker', 'soleil-18k-gold-vermeil-choker', 'Micro-Pavé Radiant Sunbeam Collar', 'Crafted in 2.5-micron 18-karat yellow gold over recycled sterling silver with hand-set stones.', '18k Yellow Gold Vermeil (Sterling Silver 925 Core)', 'Store in Anti-Tarnish Pouch', 2899.00, 3699.00, 21, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=80', 'NEW', 1, 1, 4.9, 25);

-- Product Variants
INSERT INTO `product_variants` (`variant_id`, `product_id`, `size_label`, `color`, `color_hex`, `sku`, `price`, `stock_quantity`, `is_available`) VALUES
(1, 1, 'XS', 'Midnight Black', '#111111', 'SKU-1-XS-MID', 4999.00, 8, 1),
(2, 1, 'S', 'Midnight Black', '#111111', 'SKU-1-S-MID', 4999.00, 15, 1),
(3, 1, 'M', 'Midnight Black', '#111111', 'SKU-1-M-MID', 4999.00, 12, 1),
(4, 1, 'L', 'Midnight Black', '#111111', 'SKU-1-L-MID', 4999.00, 6, 1),
(5, 1, 'S', 'Royal Emerald', '#0a4d3c', 'SKU-1-S-ROY', 5299.00, 10, 1),
(6, 1, 'M', 'Royal Emerald', '#0a4d3c', 'SKU-1-M-ROY', 5299.00, 14, 1),
(7, 2, 'S', 'Warm Camel', '#c19a6b', 'SKU-2-S-WAR', 6899.00, 10, 1),
(8, 2, 'M', 'Warm Camel', '#c19a6b', 'SKU-2-M-WAR', 6899.00, 12, 1),
(9, 2, 'L', 'Warm Camel', '#c19a6b', 'SKU-2-L-WAR', 6899.00, 5, 1),
(10, 2, 'S', 'Oatmeal Beige', '#d8cca3', 'SKU-2-S-OAT', 6899.00, 8, 1),
(11, 2, 'M', 'Oatmeal Beige', '#d8cca3', 'SKU-2-M-OAT', 6899.00, 9, 1),
(12, 3, 'XS', 'Champagne Rose', '#e7c9c0', 'SKU-3-XS-CHA', 3299.00, 7, 1),
(13, 3, 'S', 'Champagne Rose', '#e7c9c0', 'SKU-3-S-CHA', 3299.00, 14, 1),
(14, 3, 'M', 'Champagne Rose', '#e7c9c0', 'SKU-3-M-CHA', 3299.00, 11, 1),
(15, 3, 'S', 'Onyx Black', '#1a1a1a', 'SKU-3-S-ONY', 3299.00, 10, 1),
(16, 3, 'M', 'Onyx Black', '#1a1a1a', 'SKU-3-M-ONY', 3299.00, 15, 1),
(17, 4, '38R', 'Midnight Tuxedo Black', '#0a0a0a', 'SKU-4-38R-MID', 7999.00, 5, 1),
(18, 4, '40R', 'Midnight Tuxedo Black', '#0a0a0a', 'SKU-4-40R-MID', 7999.00, 8, 1),
(19, 4, '42R', 'Midnight Tuxedo Black', '#0a0a0a', 'SKU-4-42R-MID', 7999.00, 7, 1),
(20, 4, '40R', 'Deep Navy Blue', '#0d1b2a', 'SKU-4-40R-DEE', 7999.00, 6, 1),
(21, 4, '42R', 'Deep Navy Blue', '#0d1b2a', 'SKU-4-42R-DEE', 7999.00, 4, 1),
(22, 5, 'S', 'Crisp White', '#fcfcfc', 'SKU-5-S-CRI', 2499.00, 14, 1),
(23, 5, 'M', 'Crisp White', '#fcfcfc', 'SKU-5-M-CRI', 2499.00, 20, 1),
(24, 5, 'L', 'Crisp White', '#fcfcfc', 'SKU-5-L-CRI', 2499.00, 15, 1),
(25, 5, 'M', 'Sage Green', '#879f84', 'SKU-5-M-SAG', 2499.00, 12, 1),
(26, 5, 'L', 'Sage Green', '#879f84', 'SKU-5-L-SAG', 2499.00, 9, 1),
(27, 6, 'S', 'Charcoal Grey', '#36454f', 'SKU-6-S-CHA', 3899.00, 9, 1),
(28, 6, 'M', 'Charcoal Grey', '#36454f', 'SKU-6-M-CHA', 3899.00, 16, 1),
(29, 6, 'L', 'Charcoal Grey', '#36454f', 'SKU-6-L-CHA', 3899.00, 11, 1),
(30, 6, 'M', 'Alabaster Cream', '#f5f2eb', 'SKU-6-M-ALA', 3899.00, 14, 1),
(31, 6, 'L', 'Alabaster Cream', '#f5f2eb', 'SKU-6-L-ALA', 3899.00, 8, 1),
(32, 7, 'Standard', 'Espresso Cognac', '#4a2c11', 'SKU-7-Standard-ESP', 5499.00, 12, 1),
(33, 7, 'Standard', 'Carbon Black', '#111111', 'SKU-7-Standard-CAR', 5499.00, 18, 1),
(34, 8, 'Free Size', 'Havana Gold / Amber', '#784b24', 'SKU-8-Free Size-HAV', 1899.00, 25, 1),
(35, 8, 'Free Size', 'Obsidian / Gradient Grey', '#1c1c1c', 'SKU-8-Free Size-OBS', 1899.00, 20, 1),
(36, 9, 'UK 7 / EU 41', 'Mahogany Brown', '#3d1f14', 'SKU-9-UK 7 / EU 41-MAH', 6299.00, 6, 1),
(37, 9, 'UK 8 / EU 42', 'Mahogany Brown', '#3d1f14', 'SKU-9-UK 8 / EU 42-MAH', 6299.00, 10, 1),
(38, 9, 'UK 9 / EU 43', 'Mahogany Brown', '#3d1f14', 'SKU-9-UK 9 / EU 43-MAH', 6299.00, 8, 1),
(39, 9, 'UK 8 / EU 42', 'Midnight Black', '#0d0d0d', 'SKU-9-UK 8 / EU 42-MID', 6299.00, 9, 1),
(40, 9, 'UK 9 / EU 43', 'Midnight Black', '#0d0d0d', 'SKU-9-UK 9 / EU 43-MID', 6299.00, 7, 1),
(41, 10, 'UK 6 / EU 39', 'Glazed Jet Black', '#050505', 'SKU-10-UK 6 / EU 39-GLA', 5799.00, 5, 1),
(42, 10, 'UK 7 / EU 40', 'Glazed Jet Black', '#050505', 'SKU-10-UK 7 / EU 40-GLA', 5799.00, 8, 1),
(43, 10, 'UK 8 / EU 41', 'Glazed Jet Black', '#050505', 'SKU-10-UK 8 / EU 41-GLA', 5799.00, 6, 1),
(44, 11, 'Adjustable (38-45cm)', '18K Yellow Gold', '#d4af37', 'SKU-11-Adjustable (38-45cm)-18K', 2899.00, 18, 1),
(45, 11, 'Adjustable (38-45cm)', 'Platinum Rhodium', '#e5e4e2', 'SKU-11-Adjustable (38-45cm)-PLA', 2899.00, 12, 1);

-- Default Address for Patron (Sophia)
INSERT INTO `addresses` (`address_id`, `user_id`, `full_name`, `phone`, `address_line`, `landmark`, `city`, `state`, `pincode`, `is_default`, `address_type`) VALUES
(1, 2, 'Sophia Laurent', '+91 98989 12345', 'Flat 402, Royale Heights, MG Road', 'Near Central Boulevard', 'Mumbai', 'Maharashtra', '400001', 1, 'Home');

-- Reviews
INSERT INTO `reviews` (`id`, `product_id`, `user_id`, `user_name`, `rating`, `headline`, `comment`, `verified_purchase`) VALUES
(1, 1, 2, 'Claire D.', 5, 'Absolute showstopper!', 'Wore this to a charity gala and received endless compliments. The drape is breathtaking.', 1),
(2, 1, 2, 'Evelyn K.', 5, 'Flawless fit and quality', 'The velvet is heavy and expensive-feeling. Fits like a glove.', 1),
(3, 2, 2, 'Valerie S.', 5, 'So warm and chic', 'My go-to trench for autumn and winter travel. Utterly luxurious.', 1),
(4, 3, 2, 'Maya R.', 5, 'Feels like a second skin', 'The silk is extraordinarily soft and has that subtle pearlescent sheen.', 1),
(5, 4, 2, 'Marcus B.', 5, 'Bespoke level craftsmanship', 'Impeccable shoulder construction and fit. Looked unmatched at my wedding.', 1),
(6, 6, 2, 'David T.', 5, 'Perfection', 'Substantial weight without feeling bulky. Keeps you wonderfully warm.', 1),
(7, 7, 2, 'Gregory L.', 5, 'Patina develops beautifully', '6 months of daily use and the leather looks richer with each passing week.', 1),
(8, 9, 2, 'Nathan R.', 5, 'Worth every single rupee', 'The Goodyear welt construction is top tier. Broke in comfortably in just 2 days.', 1),
(9, 11, 2, 'Isabella N.', 5, 'Pure elegance', 'Dainty yet makes such a sparkling statement. Beautifully packaged in a velvet box.', 1);
