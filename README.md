markdown
Copy
# SecureAPI - Production-Level Authentication System

A complete authentication and authorization system built with FastAPI, JWT tokens, and role-based access control (RBAC).

## Features

- ✅ User Signup & Login with password hashing (Argon2)
- ✅ JWT Token-based authentication
- ✅ Refresh token mechanism for session management
- ✅ Role-Based Access Control (RBAC) - Admin, User, Mentor roles
- ✅ Protected routes with token validation
- ✅ Simple vanilla HTML/CSS/JavaScript frontend
- ✅ CORS enabled for frontend communication
- ✅ SQLite database (easily switchable to PostgreSQL)

## Project Structure
secure-api/ ├── config.py # Configuration & settings ├── database.py # Database connection setup ├── models.py # SQLAlchemy ORM models ├── schemas.py # Pydantic request/response schemas ├── auth.py # JWT & password hashing logic ├── cache.py # Redis caching (optional) ├── app.py # FastAPI application entry point ├── run.py # Server runner ├── setup.py # Database initialization ├── requirements.txt # Python dependencies ├── .env # Environment variables ├── routes/ │ ├── users.py # Signup/Login endpoints │ ├── posts.py # Protected post endpoints │ ├── admin.py # Admin-only endpoints │ └── auth.py # Refresh token & logout └── frontend/ ├── index.html # Main HTML page ├── style.css # Styling └── script.js # Frontend logic

code
Copy

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sazysid06/secure-api.git
cd secure-api
Create virtual environment:
bash
Copy
python -m venv solo
source solo/bin/activate  # On Windows: solo\Scripts\activate
Install dependencies:
bash
Copy
pip install -r requirements.txt
Setup database:
bash
Copy
python setup.py
Run the server:
bash
Copy
python run.py
Server runs at: http://localhost:8000

API Endpoints
Authentication
POST /users/signup - Create new user
POST /users/login - Login and get tokens
POST /auth/refresh - Refresh access token
POST /auth/logout - Logout
Protected Routes
GET /posts/my-posts - Get user's posts (requires token)
POST /posts/create-post - Create a post (requires token)
Admin Routes
GET /admin/users - List all users (admin only)
DELETE /admin/users/{user_id} - Delete user (admin only)
PATCH /admin/users/{user_id}/role - Change user role (admin only)
Test Credentials
Admin User:

Email: admin@example.com
Password: admin123
Regular User:

Email: john@example.com
Password: password123
Frontend
Open frontend/index.html in your browser to access the web interface.

Features:

Signup with email validation
Login with JWT token storage
Protected dashboard
View user profile & role
Logout
Technologies Used
Backend: FastAPI, SQLAlchemy, Pydantic
Authentication: JWT (JSON Web Tokens), Argon2 password hashing
Database: SQLite (development), PostgreSQL (production-ready)
Caching: Redis (optional)
Frontend: Vanilla HTML/CSS/JavaScript
API Docs: Swagger UI (available at /docs)
Key Concepts from Lecture
This project implements concepts from the "Advanced Security And Authorization" lecture:

Password Hashing: Using Argon2 (better than Bcrypt's 72-byte limit)
Token-Based Authentication: Stateless JWT tokens instead of sessions
JWT Structure: Header.Payload.Signature with signature verification
RBAC: Role-based access control for admin/user differentiation
Refresh Tokens: Long-lived tokens to renew short-lived access tokens
HTTPS Ready: Built with security best practices
Future Enhancements
 PostgreSQL integration
 Redis token blacklisting
 Email verification
 Password reset functionality
 Two-factor authentication (2FA)
 OAuth2 Google/GitHub login
 Rate limiting
 API documentation with Swagger
 Docker containerization
 Cloud deployment (AWS/Heroku)
Learning Resources
FastAPI Documentation
JWT.io
OWASP Authentication
License
MIT License - See LICENSE file for details

Author
Built as a learning project for Advanced Security & Authorization

Support
For questions or issues, please open an issue on GitHub.