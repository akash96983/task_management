from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv
from typing import List, Optional

from database import engine, get_db, Base
from models import User, Task
from schemas import (
    UserCreate, UserLogin, AuthResponse, UserResponse,
    TaskCreate, TaskUpdate, TaskResponse
)
from auth import (
    verify_password, get_password_hash, create_access_token, 
    decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware to allow Next.js frontend to connect
# Add your Vercel deployment URL to allow_origins
allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments (update with your actual URL)
]

# Get additional origins from environment variable (optional)
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get current user from token
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Task Management API!"}

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/signup", response_model=AuthResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    
    return AuthResponse(
        message="Signup successful",
        token=access_token,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at
        )
    )

@app.post("/api/auth/login", response_model=AuthResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return AuthResponse(
        message="Login successful",
        token=access_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        )
    )

# ==================== TASK ENDPOINTS ====================

@app.get("/api/tasks", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[bool] = None,
    priority: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for the current user with optional filtering and sorting"""
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # Apply filters
    if status is not None:
        query = query.filter(Task.status == status)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    # Apply sorting
    if sort_by == "created_at":
        query = query.order_by(Task.created_at.desc())
    elif sort_by == "priority":
        # Custom sorting: High > Medium > Low
        query = query.order_by(Task.priority.desc())
    elif sort_by == "status":
        query = query.order_by(Task.status)
    
    tasks = query.all()
    return tasks

@app.post("/api/tasks", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the current user"""
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        user_id=current_user.id,
        status=False  # Default to pending
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    
    db.commit()
    db.refresh(task)
    
    return task

@app.patch("/api/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_status(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle task status between pending and completed"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = not task.status
    db.commit()
    db.refresh(task)
    
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}
