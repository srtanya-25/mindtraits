# MindTraits

A full-stack web app that analyses Big Five personality traits, thinking style, and response-time behaviour, then maps the result to career suggestions. The prediction layer uses a machine learning model with a rule-based fallback.

Stack: React (Vite) frontend, Django REST Framework backend, JWT auth stored in HTTP-only cookies, PostgreSQL in production, Docker for local orchestration.

## Project Structure

```
mindtraits/
├── backend/
│   ├── mindtraits/             Django project config
│   ├── api/                    API endpoints (mixins/generics/viewsets)
│   ├── accounts/               Cookie-based JWT auth
│   ├── personality/            Question / UserResponse / PersonalityResult models
│   ├── insights/               thinking_styles / career_mapping / response_analytics
│   ├── ml_models/              Model training, prediction, SHAP
│   ├── data.json               Seed data (20 Big Five questions)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── build.sh
│
├── frontend/
│   ├── src/
│   │   ├── api/config.js        API base URL
│   │   ├── assets/css/styles.css
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── MainContent.jsx  Landing page
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── protected/
│   │   │       ├── Dashboard.jsx
│   │   │       └── TestPage.jsx
│   │   ├── App.jsx
│   │   ├── AuthProvider.jsx     Auth state via Context API
│   │   ├── axiosInstance.js     Request/response interceptors
│   │   ├── PrivateRoute.jsx
│   │   ├── PublicRoute.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── nginx.conf
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, Bootstrap 5 (CDN), Axios, React Router, FontAwesome |
| Auth | JWT in HTTP-only cookies, Axios interceptors for auto-refresh |
| Backend | Django 6, Django REST Framework |
| Database | SQLite (dev), PostgreSQL (production) |
| ML | scikit-learn, XGBoost, SHAP |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Deploy | Render (backend + frontend) |

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env with these contents:
#   SECRET_KEY=<some-50-char-string>
#   DEBUG=True
#   DATABASE_URL=sqlite:///db.sqlite3
#   FRONTEND_URL=http://localhost:5173

python manage.py migrate
python manage.py loaddata data.json    # seeds the 20 questions
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## API Endpoints (all under `/api/v1/`)

| Method | URL | Description | Auth |
|---|---|---|---|
| POST | `/register/` | Create account | Public |
| POST | `/login/` | Sets HTTP-only cookies | Public |
| POST | `/logout/` | Clears cookies | Yes |
| POST | `/refresh/` | Refresh access token from refresh cookie | Yes |
| GET | `/me/` | Current user info | Yes |
| GET | `/dashboard-protected/` | Auth check used by AuthProvider | Yes |
| GET | `/questions/` | All 20 Big Five questions | Public |
| GET, POST, PUT, DELETE | `/responses/` | User responses (ViewSet) | Yes |
| POST | `/responses/submit/` | Bulk submit all answers | Yes |
| POST | `/analyze/` | Run analysis pipeline and save result | Yes |
| GET | `/result/` | Latest result for the user | Yes |
| GET | `/results/` | Full result history | Yes |
| POST | `/token/` | SimpleJWT bearer login (for Postman/debugging) | Public |

## Docker

```bash
docker compose up --build              # start backend + frontend + postgres
docker compose down -v                 # stop and wipe the DB volume

# First-time seed inside containers:
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py loaddata data.json
docker compose exec backend python manage.py createsuperuser
```

- Frontend: http://localhost:5173 (nginx serving the built React app)
- Backend: http://localhost:8000
- Postgres: localhost:5433

## Deployment

The app deploys to Render. Backend runs as a Python web service backed by a Render PostgreSQL instance; the frontend is a static site built from `frontend/`. Pushing to `main` triggers the GitHub Actions workflow, which runs tests, builds and pushes Docker images, and calls the Render deploy hooks.

## Quick Commands

```bash
# Backend
python manage.py runserver
python manage.py migrate
python manage.py test
python manage.py loaddata data.json
python manage.py dumpdata --exclude auth.permission --exclude contenttypes \
    --exclude admin.logentry --exclude sessions > data.json

# Frontend
npm run dev
npm run build

# Docker
docker compose up --build
docker compose down -v
docker compose logs backend
docker compose exec db psql -U mindtraits_user -d mindtraits_db
```
