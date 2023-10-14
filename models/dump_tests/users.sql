DROP DATABASE IF EXISTS hustle_db;

-- Setting up MySQL database with admin user privileges.
CREATE DATABASE IF NOT EXISTS hustle_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL ON hustle_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

-- initialize database tables
USE hustle_db;


DROP TABLE IF EXISTS `users`;

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

INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `hashed_password`, `first_name`, `last_name`, `date_of_birth`, `user_image_path`, `user_video_path`, `user_banner_path`, `is_admin`, `is_active`, `is_verified`)
VALUES
    (1, NOW(), NOW(), 'user1@example.com', 'hashed_password_1', 'John', 'Doe', '1990-01-15', 'image1.jpg', 'video1.mp4', 'banner1.jpg', 0, 1, 1),
    (2, NOW(), NOW(), 'user2@example.com', 'hashed_password_2', 'Jane', 'Smith', '1985-05-20', 'image2.jpg', 'video2.mp4', 'banner2.jpg', 0, 1, 1);

INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `hashed_password`, `first_name`, `last_name`, `date_of_birth`, `user_image_path`, `user_video_path`, `user_banner_path`, `is_admin`, `is_active`, `is_verified`)
VALUES
    (3, NOW(), NOW(), 'user3@example.com', 'hashed_password_3', 'Robert', 'Johnson', '1980-09-10', 'image3.jpg', 'video3.mp4', 'banner3.jpg', 0, 1, 1),
    (4, NOW(), NOW(), 'user4@example.com', 'hashed_password_4', 'Emily', 'Davis', '1992-03-25', 'image4.jpg', 'video4.mp4', 'banner4.jpg', 0, 1, 1),
    (5, NOW(), NOW(), 'user5@example.com', 'hashed_password_5', 'Michael', 'Wilson', '1988-07-12', 'image5.jpg', 'video5.mp4', 'banner5.jpg', 0, 1, 1),
    (6, NOW(), NOW(), 'user6@example.com', 'hashed_password_6', 'Sarah', 'Martinez', '1995-11-05', 'image6.jpg', 'video6.mp4', 'banner6.jpg', 0, 1, 1),
    (7, NOW(), NOW(), 'user7@example.com', 'hashed_password_7', 'David', 'Garcia', '1984-04-30', 'image7.jpg', 'video7.mp4', 'banner7.jpg', 0, 1, 1),
    (8, NOW(), NOW(), 'user8@example.com', 'hashed_password_8', 'Olivia', 'Lopez', '1998-12-15', 'image8.jpg', 'video8.mp4', 'banner8.jpg', 0, 1, 1),
    (9, NOW(), NOW(), 'user9@example.com', 'hashed_password_9', 'William', 'Brown', '1987-06-18', 'image9.jpg', 'video9.mp4', 'banner9.jpg', 0, 1, 1),
    (10, NOW(), NOW(), 'user10@example.com', 'hashed_password_10', 'Sophia', 'Miller', '1993-02-08', 'image10.jpg', 'video10.mp4', 'banner10.jpg', 0, 1, 1);
