# Task Management App - PostgreSQL Setup Guide

## 🗄️ PostgreSQL Database Setup

### Step 1: Install PostgreSQL

**Windows:**
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Default port is `5432`

### Step 2: Create Database

Open PostgreSQL command line (psql) or pgAdmin and run:

```sql
CREATE DATABASE task_management;
```

Or using command line:
```bash
psql -U postgres
CREATE DATABASE task_management;
\q
```

### Step 3: Configure Environment Variables

Edit the `.env` file and update these values:

```env
# Replace with your PostgreSQL credentials
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/task_management

# Generate a secure secret key (run: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 4: Run the Application

The database tables will be created automatically when you start the FastAPI server:

```bash
# Start FastAPI backend
uvicorn main:app --reload --port 8000

# Start Next.js frontend (in another terminal)
npm run dev
```

## 📦 Installed Packages

### Backend (Python):
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM for database
- `psycopg2-binary` - PostgreSQL adapter
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT tokens
- `python-dotenv` - Environment variables
- `pydantic[email]` - Data validation

## 🔐 Security Features

✅ **Password Hashing** - Using bcrypt
✅ **JWT Tokens** - Secure authentication
✅ **Environment Variables** - Sensitive data protected
✅ **SQL Injection Protection** - Using SQLAlchemy ORM
✅ **CORS Configuration** - Controlled access

## 📁 Project Structure

```
task_management/
├── main.py              # FastAPI application
├── database.py          # Database connection
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── .env                 # Environment variables (DO NOT COMMIT)
├── .gitignore          # Git ignore file
├── app/                 # Next.js frontend
│   ├── auth/
│   │   ├── login/
│   │   └── signup/
│   └── dashboard/
└── package.json
```

## 🧪 Testing the API

### Signup:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

## 🔧 Troubleshooting

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists

**Import errors:**
- Reinstall packages: `pip install -r requirements.txt`

**CORS errors:**
- Check frontend URL matches in main.py
- Verify both servers are running
