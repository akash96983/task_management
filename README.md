# Task Management Application

A full-stack task management application with a **Next.js** frontend and **FastAPI** backend. Features user authentication, task CRUD operations, and a clean, responsive UI built with React and Tailwind CSS.

## Tech Stack

**Frontend:**
- Next.js 16 (React 19)
- TypeScript
- Tailwind CSS
- ESLint

**Backend:**
- FastAPI
- SQLAlchemy (ORM)
- SQLite (database)
- JWT authentication (python-jose)
- bcrypt (password hashing)
- Pydantic (validation)

## Features

- User authentication (signup/login with JWT tokens)
- Create, read, update, and delete tasks
- Secure password hashing with bcrypt
- Token-based authentication
- RESTful API with FastAPI
- Type-safe frontend with TypeScript
- Responsive UI with Tailwind CSS

## Prerequisites

- Node.js 20+ and npm
- Python 3.10+
- Git

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/akash96983/task_management.git
cd task_management
```

### 2. Backend Setup (FastAPI)

Create and activate a Python virtual environment:

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root (optional, for custom secrets):

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run the FastAPI backend:

```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000). Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

### 3. Frontend Setup (Next.js)

Install Node.js dependencies:

```bash
npm install
```

Run the Next.js development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. **Start the backend**: Run `uvicorn main:app --reload` in one terminal (with `.venv` activated)
2. **Start the frontend**: Run `npm run dev` in another terminal
3. **Sign up**: Navigate to `/auth/signup` to create an account
4. **Log in**: Navigate to `/auth/login` to authenticate
5. **Manage tasks**: Use the dashboard at `/dashboard` to create, view, update, and delete tasks

## API Endpoints

### Authentication
- `POST /signup` - Create a new user
- `POST /login` - Authenticate and receive JWT token

### Tasks (requires authentication)
- `GET /tasks` - Get all tasks for the authenticated user
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### User
- `GET /me` - Get current user profile

## Project Structure

```
task_management/
├── app/                    # Next.js app directory
│   ├── auth/              # Auth pages (login/signup)
│   ├── dashboard/         # Dashboard page
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── public/                # Static assets
├── auth.py                # JWT token & password utilities
├── database.py            # Database configuration
├── main.py                # FastAPI application
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── README.md              # This file
```

## Scripts

**Frontend:**
- `npm run dev` - Start Next.js dev server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

**Backend:**
- `uvicorn main:app --reload` - Start FastAPI dev server
- `uvicorn main:app` - Start production server

## Development

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed setup instructions and troubleshooting.

## License

MIT

## Author

[Akash](https://github.com/akash96983)
