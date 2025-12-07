# Quickstart Guide: Phase 2 - Full Web App

**Feature**: Phase 2 - Full Web App
**Date**: 2025-12-07
**Estimated Setup Time**: 15-20 minutes

## Overview

This guide walks you through setting up the Phase 2 development environment for the AI-Native Todo SaaS Platform. You'll set up the Next.js frontend, FastAPI backend, and Neon PostgreSQL database.

**What You'll Build**:
- Frontend: Next.js 14+ web application (http://localhost:3000)
- Backend: FastAPI REST API (http://localhost:8000)
- Database: Neon PostgreSQL (cloud-hosted)

---

## Prerequisites

### Required Software

1. **Node.js 18+** (for frontend)
   ```bash
   node --version  # Should be 18.x or higher
   ```
   Install: https://nodejs.org/

2. **Python 3.11+** (for backend)
   ```bash
   python --version  # Should be 3.11 or higher
   ```
   Install: https://python.org/

3. **Git** (for version control)
   ```bash
   git --version
   ```
   Install: https://git-scm.com/

### Recommended Tools

- **VS Code** with extensions:
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)
  - ESLint (dbaeumer.vscode-eslint)
  - Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- **Postman** or **Insomnia** (for API testing)

---

## Step 1: Clone Repository & Checkout Branch

```bash
# Clone repository
git clone <repository-url>
cd hackaton-2

# Checkout Phase 2 branch
git checkout 002-full-web-app

# Verify you're on the correct branch
git branch
# Should show: * 002-full-web-app
```

---

## Step 2: Database Setup (Neon PostgreSQL)

### 2.1 Create Neon Account

1. Go to https://neon.tech/
2. Sign up for free account (GitHub OAuth recommended)
3. Click "Create Project"
4. Name: `todo-saas-dev`
5. Region: Choose closest to you
6. PostgreSQL Version: 15 (default)
7. Click "Create Project"

### 2.2 Get Connection String

1. In Neon dashboard, click your project
2. Go to "Connection Details" tab
3. Copy the connection string (looks like):
   ```
   postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Save this - you'll need it for backend `.env` file

### 2.3 Verify Connection (Optional)

```bash
# Install PostgreSQL client (if not already installed)
# macOS:
brew install postgresql

# Windows:
# Download from https://www.postgresql.org/download/windows/

# Test connection
psql "postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# If successful, you'll see:
# neondb=>

# Exit with \q
```

---

## Step 3: Backend Setup (FastAPI)

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt):
.\venv\Scripts\activate.bat

# You should see (venv) in your terminal prompt
```

### 3.3 Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (pytest, etc.)
pip install -r requirements-dev.txt

# Verify installation
pip list
# Should show: fastapi, sqlalchemy, alembic, pyjwt, bcrypt, pytest, etc.
```

### 3.4 Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your favorite editor
# macOS/Linux:
nano .env

# Windows:
notepad .env
```

**Update the following in `.env`**:

```bash
# Database
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# JWT Secrets (generate random strings)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# SendGrid (for emails)
SENDGRID_API_KEY=your-sendgrid-api-key  # Get from https://sendgrid.com/
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# CORS (frontend URL)
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Generate Secure JWT Secret**:
```bash
# macOS/Linux:
openssl rand -hex 32

# Windows (PowerShell):
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### 3.5 Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic upgrade head

# You should see:
# INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

### 3.6 Run Backend Server

```bash
# Start FastAPI with hot reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Application startup complete.
```

### 3.7 Test Backend API

**Open browser**: http://localhost:8000/docs

You should see Swagger UI with all API endpoints documented.

**Test health endpoint**:
```bash
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2025-12-07T10:30:00Z"}
```

**Test registration** (via Swagger UI or curl):
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "display_name": "Test User"
  }'

# Expected response (201):
# {
#   "user": {"id": 1, "email": "test@example.com", ...},
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }
```

---

## Step 4: Frontend Setup (Next.js)

### 4.1 Navigate to Frontend Directory

**Open a NEW terminal** (keep backend running), then:

```bash
cd frontend
```

### 4.2 Install Dependencies

```bash
# Install npm packages
npm install

# Or with yarn:
yarn install

# This will install Next.js, React, TailwindCSS, axios, etc.
```

### 4.3 Configure Environment Variables

```bash
# Copy example env file
cp .env.local.example .env.local

# Edit .env.local
# macOS/Linux:
nano .env.local

# Windows:
notepad .env.local
```

**Update the following in `.env.local`**:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

### 4.4 Run Frontend Development Server

```bash
# Start Next.js dev server
npm run dev

# Or with yarn:
yarn dev

# You should see:
#   ▲ Next.js 14.x.x
#   - Local:        http://localhost:3000
#   - Ready in 2.5s
```

### 4.5 Test Frontend

**Open browser**: http://localhost:3000

You should see the landing page with:
- "Welcome to Todo SaaS" header
- Login and Register buttons
- Navigation to auth pages

**Test registration flow**:
1. Click "Register"
2. Fill in form (email, password, display name)
3. Submit
4. Should redirect to dashboard with "No tasks yet" message

**Test login flow**:
1. Click "Login"
2. Enter registered email and password
3. Submit
4. Should redirect to dashboard

---

## Step 5: Run Tests

### 5.1 Backend Tests

```bash
# In backend directory (with venv activated)
cd backend

# Run all tests
pytest tests/ -v

# Run specific test types
pytest tests/unit/ -v              # Unit tests only
pytest tests/integration/ -v        # Integration tests only

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Open coverage report
# macOS/Linux:
open htmlcov/index.html

# Windows:
start htmlcov/index.html
```

**Expected output**:
```
============================= test session starts ==============================
platform darwin -- Python 3.11.6, pytest-7.4.3
collected 45 items

tests/unit/test_auth_service.py::test_hash_password PASSED                [ 2%]
tests/unit/test_auth_service.py::test_verify_password PASSED              [ 4%]
...
tests/integration/test_auth_endpoints.py::test_register_success PASSED    [95%]
tests/integration/test_task_endpoints.py::test_create_task PASSED         [100%]

============================== 45 passed in 5.23s ===============================
```

### 5.2 Frontend Tests

```bash
# In frontend directory
cd frontend

# Run Jest unit tests
npm run test

# Or with yarn:
yarn test

# Run E2E tests with Playwright (if implemented)
npm run test:e2e
```

---

## Step 6: Migrate Phase 1 Data (Optional)

If you have Phase 1 JSON data (`tasks.json`), migrate it to PostgreSQL:

```bash
# In project root
python scripts/migrate-phase1-data.py tasks.json

# Expected output:
# Created migration user: phase1-migration@example.com
# Migrated 5 tasks from Phase 1
# Migration complete!
```

**Verify migration**:
```bash
# Via API
curl http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <access_token>"

# Or via psql
psql "postgresql://..." -c "SELECT COUNT(*) FROM tasks;"
# Should show: 5
```

---

## Development Workflow

### Typical Day-to-Day

1. **Start backend** (in backend directory):
   ```bash
   source venv/bin/activate  # Activate venv
   uvicorn src.main:app --reload --port 8000
   ```

2. **Start frontend** (in frontend directory, separate terminal):
   ```bash
   npm run dev
   ```

3. **Make changes** to code (hot reload enabled for both)

4. **Run tests** before committing:
   ```bash
   # Backend
   cd backend && pytest tests/ -v

   # Frontend
   cd frontend && npm run test
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add task filtering by priority"
   git push origin 002-full-web-app
   ```

### Database Migrations

When you modify SQLAlchemy models:

```bash
# In backend directory
cd backend

# Generate migration (auto-detect changes)
alembic revision --autogenerate -m "Add tags to tasks"

# Review generated migration in src/db/migrations/versions/

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Activate virtual environment: `source venv/bin/activate`

**Problem**: `psycopg2.OperationalError: could not connect to server`
- **Solution**: Verify DATABASE_URL in `.env`, check Neon connection string, ensure network connectivity

**Problem**: `sqlalchemy.exc.ProgrammingError: relation "users" does not exist`
- **Solution**: Run migrations: `alembic upgrade head`

**Problem**: `pydantic.error_wrappers.ValidationError: validation error for RegisterRequest`
- **Solution**: Check request body format in Swagger UI or curl command, ensure required fields present

### Frontend Issues

**Problem**: `Error: Cannot find module 'next'`
- **Solution**: Run `npm install` in frontend directory

**Problem**: `TypeError: Cannot read property 'map' of undefined`
- **Solution**: Check API response format, ensure backend is running on port 8000

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`
- **Solution**: Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`

**Problem**: `401 Unauthorized` on API requests
- **Solution**: Check JWT token in Authorization header, verify token not expired (24h), use `/auth/refresh` if needed

### Database Issues

**Problem**: `FATAL: password authentication failed for user "xxx"`
- **Solution**: Verify Neon connection string, regenerate password in Neon dashboard if needed

**Problem**: `FATAL: remaining connection slots are reserved`
- **Solution**: Neon free tier has 1 concurrent connection limit, close idle connections

**Problem**: `SSL connection has been closed unexpectedly`
- **Solution**: Ensure `?sslmode=require` in DATABASE_URL, check network stability

---

## Next Steps

### Phase 2 Implementation Tasks

Once setup is complete, proceed with implementation:

1. **Generate tasks.md**: Run `/sp.tasks` command to create implementation task list
2. **Follow TDD workflow**: Write tests → Implement → Tests pass
3. **Complete user stories** in priority order (P1 → P5)
4. **Regular commits**: Commit working increments to `002-full-web-app` branch

### Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Neon Docs**: https://neon.tech/docs/
- **Phase 2 Spec**: [spec.md](./spec.md)
- **Phase 2 Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/api-endpoints.md](./contracts/api-endpoints.md)

### Getting Help

- **Slack/Discord**: #phase-2-dev channel
- **GitHub Issues**: https://github.com/your-org/hackaton-2/issues
- **Project Lead**: @username

---

**Quickstart Guide Complete**: 2025-12-07
**Ready to Start Development!** 🚀
