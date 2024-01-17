-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th1 17, 2024 lúc 04:00 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `vegetablememory`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `products`
--

CREATE TABLE `products` (
  `name` varchar(50) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `image_url` text DEFAULT NULL,
  `stock_quantity` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `products`
--

INSERT INTO `products` (`name`, `price`, `description`, `image_url`, `stock_quantity`, `category_id`, `id`, `created_at`, `updated_at`) VALUES
('Cà rốt tươi', 2, 'Cà rốt xanh mướt', 'carrot.jpg', 100, 1, 1, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Cà chua đỏ', 3, 'Cà chua chín đỏ', 'tomato.jpg', 120, 2, 2, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Bông cải xanh', 2, 'Bông cải non tươi', 'broccoli.jpg', 80, 3, 3, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Dưa leo mát', 1, 'Dưa leo xanh mát', 'cucumber.jpg', 150, 4, 4, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Ớt chuông đủ màu', 4, 'Ớt chuông đỏ, vàng, xanh', 'pepper.jpg', 90, 5, 5, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Rau cải xanh', 2, 'Rau cải xanh non tươi', 'spinach.jpg', 110, 6, 6, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Khoai tây sắc màu', 5, 'Khoai tây màu sắc đa dạng', 'potato.jpg', 70, 7, 7, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Hành tây thơm', 2, 'Hành tây thơm ngon', 'onion.jpg', 130, 8, 8, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Tỏi hữu ích', 3, 'Tỏi chất lượng cao', 'garlic.jpg', 100, 9, 9, '2024-01-17 02:21:25', '2024-01-17 02:21:25'),
('Rau xà lách xanh', 2, 'Rau xà lách xanh tươi', 'lettuce.jpg', 120, 10, 10, '2024-01-17 02:21:25', '2024-01-17 02:21:25');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_products_name` (`name`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `ix_products_id` (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
