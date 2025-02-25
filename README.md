██████╗ ██████╗  ██████╗ ██╗  ██╗██████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔══██╗██╔════╝██╔════╝
██████╔╝██████╔╝██║   ██║█████╔╝ ██████╔╝█████╗  ███████╗
██╔══██╗██╔══██╗██║   ██║██╔═██╗ ██╔══██╗██╔══╝  ╚════██║
██████╔╝██║  ██║╚██████╔╝██║  ██╗██║  ██║███████╗███████║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

=======================
  SYSTEM ARCHITECTURE 
=======================
Components:
• Event Bus (RabbitMQ) 
• Transactional DB (PostgreSQL)
• Read DB (MongoDB) 
• Cache/Queue (Redis)
• Background Workers (3)

Data Flow:
Client → API → Service → RabbitMQ → Workers → DBs

=======================
  COMPLETE ENDPOINTS 
=======================

[ AUTHENTICATION ]
POST   /signup             # Register new user (phone/email/password)
POST   /login              # Initiate OTP flow (returns user_identifier)
POST   /verify-otp         # Validate OTP → returns JWT tokens
POST   /refresh            # Refresh access token using refresh token

[ BOOK MANAGEMENT ]
GET    /books              # List all books (paginated)
POST   /books              # Add new book (admin only)
GET    /books/{id}         # Get book details
PUT    /books/{id}         # Update book info (admin)
DELETE /books/{id}         # Remove book (admin)
GET    /books/search       # Full-text search (MongoDB)

[ RESERVATIONS ]
POST   /reserve            # Create reservation
GET    /reservations       # List reservations (admin/user-specific)
GET    /reservations/{id}  # Get reservation details
PUT    /reservations/{id}  # Modify reservation dates
DELETE /reservations/{id}  # Cancel reservation
POST   /return/{id}        # Return book + process queue

[ USER MANAGEMENT ]
GET    /users              # List users (admin)
GET    /users/{id}         # Get user profile
PUT    /users/{id}         # Update profile
DELETE /users/{id}         # Delete account (admin/user)
POST   /users/charge       # Add wallet funds
PUT    /users/subscription # Change subscription tier

=======================
  KEY FEATURES 
=======================
1. Event-Driven Architecture
   • RabbitMQ message broker
   • Outbox pattern for DB sync
   • 3 background workers

2. Subscription Tiers
   • FREE: 1 book/week
   • PLUS ($5/mo): 3 books/week
   • PREMIUM ($15/mo): Unlimited

3. Priority Queue System
   • Redis-sorted sets
   • Priority: PREMIUM > PLUS > FREE
   • Auto-notification when available

4. Multi-DB Consistency
   • PostgreSQL: Transactions
   • MongoDB: Read-optimized
   • Sync via outbox processor

=======================
  SETUP & RUNNING 
=======================
1. Environment:
   DB_HOST=postgres
   DB_USER=bookadmin
   DB_PASSWORD=securepass123
   RABBITMQ_URI=amqp://guest:guest@rabbitmq

2. Start Services:
   docker-compose up --build

3. Initialize DB:
   alembic upgrade head
   python insert_sample.py

4. Access Points:
   • API Docs: http://localhost:8000/docs
   • RabbitMQ Dashboard: http://localhost:15672
   • PGAdmin: http://localhost:5433

=======================
  SECURITY 
=======================
• JWT Authentication (HS256)
• OTP Verification (Redis-stored)
• Role-Based Access Control

=======================
  LICENSE 
=======================
MIT License | © 2024 BookReserve Team
