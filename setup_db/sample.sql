INSERT INTO users(username,first_name,last_name,phone,user_password,email,user_role) VALUES
('admin1', 'Ali', 'Rezaei', '09123456789', 'ali912','admin1@example.com', 'ADMIN'),
('customer1', 'Sara', 'Moradi', '09123456788', 'saramoradi','customer1@example.com', 'CUSTOMER'),
('author1', 'Mohammad', 'Ahmadi', '09123456787', '6787ahmadi','author1@example.com', 'AUTHOR'),
('customer2', 'Reza', 'Hosseini', '09123456786', 'reza6786','customer2@example.com', 'CUSTOMER'),
('author2', 'Fatemeh', 'Karimi', '09123456785', '1403fateme','author2@example.com', 'AUTHOR'),
('customer3', 'Zahra', 'Alavi', '09123456784', 'zahala','customer3@example.com', 'CUSTOMER'),
('admin2', 'Hossein', 'Mohammadi', '09123456783', '@hossein','admin2@example.com', 'ADMIN'),
('author3', 'Maryam', 'Sadeghi', '09123456782', 'maryam6782','author3@example.com', 'AUTHOR'),
('customer4', 'Amir', 'Rahimi', '09123456781', 'amirrahimi6781','customer4@example.com', 'CUSTOMER'),
('author4', 'Narges', 'Gholami', '09123456780', 'narges6780','author4@example.com', 'AUTHOR');

INSERT INTO cities (city_name) VALUES
('Tehran'),
('Urmia'),
('Neyshabour'),
('New York'),
('Sydney'),
('Berlin'),
('Moscow'),
('Beijing'),
('Ankara'),
('Rio de Janeiro');

INSERT INTO authors (id, city_id, goodreads_link, bank_account) VALUES
(1, 1, 'https://www.goodreads.com/author1', '123456789012'),
(2, 3, 'https://www.goodreads.com/author2', '987654321098'),
(3, 5, 'https://www.goodreads.com/author3', '456789012345'),
(4, 2, 'https://www.goodreads.com/author4', '321098765432'),
(5, 4, 'https://www.goodreads.com/author5', '654321098765'),
(6, 6, 'https://www.goodreads.com/author6', '789012345678'),
(7, 7, 'https://www.goodreads.com/author7', '890123456789'),
(8, 8, 'https://www.goodreads.com/author8', '901234567890'),
(9, 9, 'https://www.goodreads.com/author9', '012345678901'),
(10, 10, 'https://www.goodreads.com/author10', '234567890123');

INSERT INTO customers(id, sub_model, subscription_end, wallet) VALUES
(1, 'FREE', '2024-12-31 23:59:59', 120000),
(2, 'PLUS', '2025-06-30 23:59:59', 200000),
(3, 'PREMIUM', '2024-10-15 23:59:59', 0),
(4, 'FREE', '2024-11-30 23:59:59', 26000),
(5, 'PLUS', '2025-01-31 23:59:59', 50000),
(6, 'PREMIUM', '2024-09-30 23:59:59', 100000),
(7, 'FREE', '2024-08-31 23:59:59', 15000),
(8, 'PLUS', '2025-03-31 23:59:59', 2000),
(9, 'PREMIUM', '2024-07-31 23:59:59', 1000000),
(10, 'FREE', '2024-12-31 23:59:59', 44000);

INSERT INTO genres (gen_name) VALUES
('Science Fiction'),
('Fantasy'),
('Mystery'),
('Thriller'),
('Romance'),
('Historical Fiction'),
('Horror'),
('Non-Fiction'),
('Biography'),
('Young Adult');

INSERT INTO books (title, isbn, price, genre_id, book_desc, units, author_id) VALUES
('The Great Gatsby', '9780743273565', 14000, 5, 'A classic novel about the American Dream.', 10, 1),
('1984', '9780451524935', 90000, 2, 'A dystopian novel about totalitarianism.', 5, 2),
('To Kill a Mockingbird', '9780061120084', 99000, 6, 'A story of racial injustice in the American South.', 100, 3),
('Pride and Prejudice', '9780141439518', 80000, 5, 'A romantic novel set in Regency England.', 12, 4),
('The Hobbit', '9780547928227', 40000, 2, 'A fantasy adventure novel.', 2, 5),
('The Da Vinci Code', '9780307474278', 14000, 4, 'A thriller involving art and secret societies.', 40, 6),
('The Shining', '9780307743657', 20000, 7, 'A horror novel about a haunted hotel.', 70, 7),
('Sapiens: A Brief History of Humankind', '9780062316097', 19000, 8, 'A non-fiction book about human history.', 250, 8),
('Becoming', '9781524763138', 13500, 9, 'A memoir by Michelle Obama.', 300, 9),
('The secret of our success', '9780439023481', 1000, 1, 'A ', 1, 10);

INSERT INTO reservations (customer_id, book_id, start_time, end_time) VALUES
(1, 1, '2023-10-01 10:00:00', '2023-10-08 10:00:00'),
(2, 2, '2023-10-02 11:00:00', '2023-10-09 11:00:00'),
(3, 3, '2023-10-03 12:00:00', '2023-10-10 12:00:00'),
(4, 4, '2023-10-04 13:00:00', '2023-10-11 13:00:00'),
(5, 5, '2023-10-05 14:00:00', '2023-10-12 14:00:00'),
(6, 6, '2023-10-06 15:00:00', '2023-10-13 15:00:00'),
(7, 7, '2023-10-07 16:00:00', '2023-10-14 16:00:00'),
(8, 8, '2023-10-08 17:00:00', '2023-10-15 17:00:00'),
(9, 9, '2023-10-09 18:00:00', '2023-10-16 18:00:00'),
(10, 10, '2023-10-10 19:00:00', '2023-10-17 19:00:00');