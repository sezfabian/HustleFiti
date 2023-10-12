CREATE DATABASE IF NOT EXISTS hustle_db;
-- Seting up mysql database with admin user privileges.
USE hustle_db;
-- Initializing database tables.

-- users table
CREATE TABLE IF NOT EXISTS `users`(
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `email` VARCHAR(45) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(45) NOT NULL,
    `last_name` VARCHAR(45) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `gender` VARCHAR(45) NOT NULL,
    `phone_number` VARCHAR(45),
    `user_image_path` VARCHAR(255),
    `user_video_path` VARCHAR(255),
    `user_banner_path` VARCHAR(255),
    `is_admin` BOOLEAN DEFAULT FALSE NOT NULL,
    `is_active` BOOLEAN DEFAULT TRUE NOT NULL,
    `is_verified` BOOLEAN DEFAULT FALSE NOT NULL,
    `session_id` VARCHAR(250),
    `reset_token` VARCHAR(250),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `service_categories`(
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `sub_categories` VARCHAR(255),
    PRIMARY KEY (`id`)
);

-- services table
CREATE TABLE IF NOT EXISTS `services`(
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

CREATE TABLE IF NOT EXISTS `price_packages`(
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

-- contracts table
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

-- payments table
CREATE TABLE IF NOT EXISTS `payments`(
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