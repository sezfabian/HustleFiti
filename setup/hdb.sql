-- Setting up a MySQL database with admin user privileges
CREATE DATABASE IF NOT EXISTS hustle_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON hustle_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

-- Initializing database tables
USE hustle_db;

-- Users table
CREATE TABLE IF NOT EXISTS `users` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `email` VARCHAR(45) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(45) NOT NULL,
    `last_name` VARCHAR(45) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `user_image_path` VARCHAR(255),
    `user_video_path` VARCHAR(255),
    `user_banner_path` VARCHAR(255),
    `is_admin` BOOLEAN NOT NULL,
    `is_active` BOOLEAN NOT NULL,
    `is_verified` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
);

-- Service Categories table
CREATE TABLE IF NOT EXISTS `service_categories` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `sub_categories` VARCHAR(255),
    PRIMARY KEY (`id`)
);

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

-- Contracts table
CREATE TABLE IF NOT EXISTS `contracts` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` VARCHAR(45) NOT NULL,
    `service_id` VARCHAR(45) NOT NULL,
    `location` VARCHAR(45) NOT NULL,
    `duration` VARCHAR(45),
    `price_package_id` VARCHAR(45) NOT NULL,
    `total_amount` DECIMAL(10,2),
    `contract_start_date` DATETIME,
    `contract_end_date` DATETIME,
    `contract_status` VARCHAR(45) NOT NULL,
    `paid_amount` DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`) ON DELETE CASCADE
);

-- Payments table
CREATE TABLE IF NOT EXISTS `payments` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` VARCHAR(45) NOT NULL,
    `contract_id` VARCHAR(45) NOT NULL,
    `amount` DECIMAL(10,2) NOT NULL,
    `payment_method` VARCHAR(45) NOT NULL,
    `transaction_id` VARCHAR(45) NOT NULL,
    `phone_number` VARCHAR(45),
    `email` VARCHAR(45),
    `account_number` VARCHAR(45),
    `bank` VARCHAR(45),
    `payment_status` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`contract_id`) REFERENCES `contracts`(`id`) ON DELETE CASCADE
);

-- Service Reviews table
CREATE TABLE IF NOT EXISTS `service_reviews` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `user_id` VARCHAR(45) NOT NULL,
    `contract_id` VARCHAR(45) NOT NULL,
    `service_id` VARCHAR(45) NOT NULL,
    `rating` DECIMAL(10,2) NOT NULL,
    `comment` VARCHAR(255),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`contract_id`) REFERENCES `contracts`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`) ON DELETE CASCADE
);

-- Client Reviews table
CREATE TABLE IF NOT EXISTS `client_reviews` (
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `contract_id` VARCHAR(45) NOT NULL,
    `user_id` VARCHAR(45) NOT NULL,
    `rating` DECIMAL(10,2) NOT NULL,
    `comment` VARCHAR(255),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`contract_id`) REFERENCES `contracts`(`id`) ON DELETE CASCADE
);

