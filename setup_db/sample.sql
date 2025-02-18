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
(3, 1, 'https://www.goodreads.com/author1', '123456789012'),
(5, 3, 'https://www.goodreads.com/author2', '987654321098'),
(8, 5, 'https://www.goodreads.com/author3', '456789012345'),
(10, 2, 'https://www.goodreads.com/author4', '321098765432');

INSERT INTO customers(id, sub_model, subscription_end, wallet) VALUES
(2, 'FREE', '2025-12-31 23:59:59', 12000000),
(4, 'PLUS', '2025-06-30 23:59:59', 20000000),
(6, 'PREMIUM', '2025-10-15 23:59:59', 10000000),
(9, 'FREE', '2025-11-30 23:59:59', 2600000);

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
('The Great Gatsby', '9780743273565', 14000, 5, 'A classic novel about the American Dream.', 10, 3),
('1984', '9780451524935', 90000, 3, 'A dystopian novel about totalitarianism.', 0, 3),
('To Kill a Mockingbird', '9780061120084', 99000, 5, 'A story of racial injustice in the American South.', 100, 5),
('Pride and Prejudice', '9780141439518', 80000, 5, 'A romantic novel set in Regency England.', 12, 5),
('The Hobbit', '9780547928227', 40000, 2, 'A fantasy adventure novel.', 2, 5),
('The Da Vinci Code', '9780307474278', 14000, 4, 'A thriller involving art and secret societies.', 40, 8),
('The Shining', '9780307743657', 20000, 7, 'A horror novel about a haunted hotel.', 70, 8),
('Sapiens: A Brief History of Humankind', '9780062316097', 19000, 8, 'A non-fiction book about human history.', 250, 8),
('Becoming', '9781524763138', 13500, 9, 'A memoir by Michelle Obama.', 300, 10),
('The secret of our success', '9780439023481', 1000, 1, 'A ', 1, 10);

INSERT INTO reservations (customer_id, book_id, start_time, end_time,price) VALUES
(6, 2, '2025-2-16 19:00:00', '2025-2-27 19:00:00',11000);