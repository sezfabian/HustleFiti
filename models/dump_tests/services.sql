
-- Setting up a MySQL database with admin user privileges
CREATE DATABASE IF NOT EXISTS hustle_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON hustle_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

-- Initializing database tables
USE hustle_db;

DROP TABLE IF EXISTS `service_category`;


-- Service Categories table
CREATE TABLE IF NOT EXISTS `service_categories` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `sub_categories` VARCHAR(255),
    PRIMARY KEY (`id`)
);

-- Sample Data for the `service_categories` table with numeric IDs
INSERT INTO `service_categories` (`id`, `created_at`, `updated_at`, `name`, `sub_categories`)
VALUES
    (1, NOW(), NOW(), 'Category 1', 'Subcategory A, Subcategory B'),
    (2, NOW(), NOW(), 'Category 2', 'Subcategory C, Subcategory D'),
    (3, NOW(), NOW(), 'Category 3', 'Subcategory E, Subcategory F'),
    (4, NOW(), NOW(), 'Category 4', 'Subcategory G, Subcategory H'),
    (5, NOW(), NOW(), 'Category 5', 'Subcategory I, Subcategory J'),
    (6, NOW(), NOW(), 'Category 6', 'Subcategory K, Subcategory L'),
    (7, NOW(), NOW(), 'Category 7', 'Subcategory M, Subcategory N'),
    (8, NOW(), NOW(), 'Category 8', 'Subcategory O, Subcategory P'),
    (9, NOW(), NOW(), 'Category 9', 'Subcategory Q, Subcategory R'),
    (10, NOW(), NOW(), 'Category 10', 'Subcategory S, Subcategory T');


DROP TABLE IF EXISTS `services`;

-- Services table
CREATE TABLE IF NOT EXISTS `services` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` VARCHAR(45) NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255),
    `service_category_id` VARCHAR(45),
    `image_paths` VARCHAR(255),
    `video_paths` VARCHAR(255),
    `banner_paths` VARCHAR(255),
    `is_verified` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`service_category_id`) REFERENCES `service_categories`(`id`) ON DELETE SET NULL
);

-- Sample Data for the `services` table
INSERT INTO `services` (`id`, `created_at`, `updated_at`, `user_id`, `name`, `description`, `service_category_id`, `image_paths`, `video_paths`, `banner_paths`, `is_verified`)
VALUES
    ('1', NOW(), NOW(), '1', 'Service 1', 'Service 1 Description', '1', 'image1.jpg', 'video1.mp4', 'banner1.jpg', 1),
    ('2', NOW(), NOW(), '2', 'Service 2', 'Service 2 Description', '2', 'image2.jpg', 'video2.mp4', 'banner2.jpg', 1),
    ('3', NOW(), NOW(), '3', 'Service 3', 'Service 3 Description', '1', 'image3.jpg', 'video3.mp4', 'banner3.jpg', 1),
    ('4', NOW(), NOW(), '4', 'Service 4', 'Service 4 Description', '2', 'image4.jpg', 'video4.mp4', 'banner4.jpg', 1),
    ('5', NOW(), NOW(), '5', 'Service 5', 'Service 5 Description', '1', 'image5.jpg', 'video5.mp4', 'banner5.jpg', 1),
    ('6', NOW(), NOW(), '6', 'Service 6', 'Service 6 Description', '2', 'image6.jpg', 'video6.mp4', 'banner6.jpg', 1),
    ('7', NOW(), NOW(), '7', 'Service 7', 'Service 7 Description', '1', 'image7.jpg', 'video7.mp4', 'banner7.jpg', 1),
    ('8', NOW(), NOW(), '8', 'Service 8', 'Service 8 Description', '2', 'image8.jpg', 'video8.mp4', 'banner8.jpg', 1),
    ('9', NOW(), NOW(), '9', 'Service 9', 'Service 9 Description', '1', 'image9.jpg', 'video9.mp4', 'banner9.jpg', 1),
    ('10', NOW(), NOW(), '10', 'Service 10', 'Service 10 Description', '2', 'image10.jpg', 'video10.mp4', 'banner10.jpg', 1);


DROP TABLE IF EXISTS `price_packages`;


-- Price Packages table
CREATE TABLE IF NOT EXISTS `price_packages` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `service_id` VARCHAR(45) NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `price` DECIMAL(10,2) NOT NULL,
    `duration` VARCHAR(45),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`) ON DELETE CASCADE
);


-- Sample Data for the `price_packages` table
INSERT INTO `price_packages` (`id`, `created_at`, `updated_at`, `service_id`, `name`, `description`, `price`, `duration`)
VALUES
    (1, NOW(), NOW(), 1, 'Package 1', 'Package 1 Description', 100.00, '1 hour'),
    (2, NOW(), NOW(), 1, 'Package 2', 'Package 2 Description', 150.00, '2 hours'),
    (3, NOW(), NOW(), 2, 'Package 3', 'Package 3 Description', 75.00, '45 minutes'),
    (4, NOW(), NOW(), 2, 'Package 4', 'Package 4 Description', 120.00, '1.5 hours'),
    (5, NOW(), NOW(), 3, 'Package 5', 'Package 5 Description', 80.00, '1 hour'),
    (6, NOW(), NOW(), 3, 'Package 6', 'Package 6 Description', 110.00, '1.25 hours'),
    (7, NOW(), NOW(), 4, 'Package 7', 'Package 7 Description', 200.00, '3 hours'),
    (8, NOW(), NOW(), 4, 'Package 8', 'Package 8 Description', 250.00, '4 hours'),
    (9, NOW(), NOW(), 5, 'Package 9', 'Package 9 Description', 90.00, '1.5 hours'),
    (10, NOW(), NOW(), 5, 'Package 10', 'Package 10 Description', 130.00, '2.5 hours');

