from pathlib import Path
import os
from dotenv import load_dotenv

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = "django-insecure-2h(^%6ite%if(+dqhhq(u%o9ted@yaqw3ncut)61wb$ors*$c@"
DEBUG = True
ALLOWED_HOSTS = []

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tickets",
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# URLS / WSGI
# --------------------------------------------------
ROOT_URLCONF = "supportdesk.urls"
WSGI_APPLICATION = "supportdesk.wsgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "tickets" / "templates",
        ],
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

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# LANGUAGE / TIMEZONE
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------
# AUTH REDIRECTS
# --------------------------------------------------
LOGIN_REDIRECT_URL = "/tickets/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
LOGIN_URL = "/accounts/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==================================================
# MICROSOFT GRAPH (OPTION 2 – RECOMMENDED)
# ==================================================
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MAILBOX_USER = os.getenv("MAILBOX_USER")

# ==================================================
# SMTP (SEND EMAILS / AUTO RESPONSES)
# ==================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("MAILBOX_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==================================================
# OPTIONAL IMAP (ONLY IF YOU STILL WANT IT)
# ==================================================
EMAIL_HOST_IMAP = "outlook.office365.com"
EMAIL_PORT_IMAP = 993
EMAIL_USE_SSL_IMAP = True
EMAIL_FOLDER = "INBOX"

# ==============================
# AZURE AD (Microsoft Entra ID)
# ==============================

AZURE_TENANT_ID = "8f58f9d9-51f4-4348-bd4a-f8b1e9030438"
AZURE_CLIENT_ID = "f0b26296-9cd3-40ed-bbc7-058c3b407a8d"
AZURE_CLIENT_SECRET = "pdK8Q~Y4igCyW.HX7iR7GV1bqPIZnR6yW~0elat6"
