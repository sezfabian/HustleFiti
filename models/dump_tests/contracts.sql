
-- Setting up a MySQL database with admin user privileges
CREATE DATABASE IF NOT EXISTS hustle_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON hustle_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

USE hustle_db;


DROP TABLE IF EXISTS `contracts`;

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




-- Sample Data for the `contracts` table
INSERT INTO `contracts` (`id`, `created_at`, `updated_at`, `user_id`, `service_id`, `location`, `duration`, `price_package_id`, `total_amount`, `contract_start_date`, `contract_end_date`, `contract_status`, `paid_amount`)
VALUES
    (1, NOW(), NOW(), 1, 1, 'Location 1', '1 hour', 1, 100.00, NOW(), NOW(), 'Active', 100.00),
    (2, NOW(), NOW(), 2, 2, 'Location 2', '2 hours', 2, 200.00, NOW(), NOW(), 'Active', 200.00),
    (3, NOW(), NOW(), 3, 3, 'Location 3', '1.5 hours', 3, 75.00, NOW(), NOW(), 'Active', 75.00),
    (4, NOW(), NOW(), 4, 4, 'Location 4', '2.5 hours', 4, 250.00, NOW(), NOW(), 'Active', 250.00),
    (5, NOW(), NOW(), 5, 5, 'Location 5', '1.25 hours', 5, 110.00, NOW(), NOW(), 'Active', 110.00),
    (6, NOW(), NOW(), 6, 6, 'Location 6', '3 hours', 6, 300.00, NOW(), NOW(), 'Active', 300.00),
    (7, NOW(), NOW(), 7, 7, 'Location 7', '2 hours', 7, 220.00, NOW(), NOW(), 'Active', 220.00),
    (8, NOW(), NOW(), 8, 8, 'Location 8', '4.5 hours', 8, 450.00, NOW(), NOW(), 'Active', 450.00),
    (9, NOW(), NOW(), 9, 9, 'Location 9', '1.75 hours', 9, 130.00, NOW(), NOW(), 'Active', 130.00),
    (10, NOW(), NOW(), 10, 10, 'Location 10', '5 hours', 10, 500.00, NOW(), NOW(), 'Active', 500.00);

