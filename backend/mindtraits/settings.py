"""
Django settings for MindTraits project.
Pattern: decouple for .env, dj_database_url for DB,
HTTP-only cookie JWT auth.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config("SECRET_KEY")
DEBUG      = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    config("RENDER_EXTERNAL_HOSTNAME", default=""),
]

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    # Local apps
    "accounts",
    "personality",
    "api",
]

# Middleware 
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # serves static files in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF       = "mindtraits.urls"
WSGI_APPLICATION   = "mindtraits.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database 
# DATABASE_URL drives everything:
#   sqlite:///db.sqlite3   for local dev
#   postgresql://    for Render production
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

#  Static files (whitenoise serves them in prod) 
STATIC_URL          = "/static/"
STATIC_ROOT         = BASE_DIR / "staticfiles"
STATICFILES_DIRS    = []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# DRF 
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "SEARCH_PARAM": "q",
    "ORDERING_PARAM": "sort_by",
    "DEFAULT_AUTHENTICATION_CLASSES": ["accounts.authentication.CookieJWTAuthentication"],
}

# JWT 
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
}

#  CORS 
# Required because frontend (port 5173) and backend (port 8000) are different origins
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    origin for origin in [
        "http://localhost:5173",
        config("FRONTEND_URL", default="http://localhost:5173"),
    ] if origin
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

#  Cookie security (secure in production, lenient in dev) 
CSRF_COOKIE_SECURE     = not DEBUG
SESSION_COOKIE_SECURE  = not DEBUG
CSRF_COOKIE_SAMESITE   = "None"
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_HTTPONLY   = False    # frontend JS needs to read CSRF token if used
SESSION_COOKIE_HTTPONLY = True
