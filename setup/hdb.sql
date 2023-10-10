-- Seting up mysql database with admin user privileges.
CREATE DATABASE IF NOT EXISTS hustle_db;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123'; 
GRANT ALL PRIVILEGES ON hustle_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

-- initialize database tables.
USE hustle_db;

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
    `user_image_path` VARCHAR(255),
    `user_video_path` VARCHAR(255),
    `user_banner_path` VARCHAR(255),
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

CREATE TABLE IF NOT EXISTS `price_packages`(
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `price` DECIMAL(10,2) NOT NULL,
    `duration` VARCHAR(45),
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS `services`(
    `id` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255),
    `price_packages_id` VARCHAR(45),
    `service_category_id` VARCHAR(45),
    `image_paths` VARCHAR(255),
    `video_paths` VARCHAR(255),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`service_category_id`) REFERENCES `service_categories`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`price_packages_id`) REFERENCES `price_packages`(`id`) ON DELETE SET NULL
);
