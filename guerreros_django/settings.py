"""
Configuración del proyecto Django — Academia Guerreros CF Yauhquemehcan
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-cambia-esta-clave-antes-de-produccion")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*").split(",")

# ── CLOUDINARY (almacenamiento de imágenes en la nube) ──
# Si defines estas 3 variables (en tu archivo .env o en el panel de tu
# hosting), las fotos subidas desde el admin se guardan en Cloudinary en
# vez del disco local. Esto es indispensable en hostings como Render,
# Railway o Heroku, donde el disco se borra cada vez que el servidor
# reinicia. Si las dejas vacías, el sitio sigue funcionando igual que
# antes (guardando todo en la carpeta media/ del servidor).
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY", default="")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", default="")
USAR_CLOUDINARY = bool(CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

if USAR_CLOUDINARY:
    INSTALLED_APPS += ["cloudinary_storage"]
    INSTALLED_APPS += ["cloudinary"]

INSTALLED_APPS += ["core"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "guerreros_django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "guerreros_django.wsgi.application"
ASGI_APPLICATION = "guerreros_django.asgi.application"

# ── BASE DE DATOS ──
# En tu computadora usa SQLite (archivo local, cero configuración).
# En producción (Render, Railway, etc.) define la variable de entorno
# DATABASE_URL con tu base de datos PostgreSQL y se usa automáticamente.
# ¡Importante!: en hostings con disco temporal, SQLite se borra en cada
# reinicio, así que en producción SIEMPRE necesitas una base de datos
# externa (Postgres) — no dejes esto en SQLite si el sitio ya es público.
import dj_database_url

DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# ── ARCHIVOS ESTÁTICOS (CSS/JS) ──
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static_global"] if (BASE_DIR / "static_global").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
# Whitenoise sirve el CSS/JS directamente desde Django sin necesitar Nginx,
# con cache y compresión — ideal para Render/Railway/Heroku.
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USAR_CLOUDINARY
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATICFILES_STORAGE = STORAGES["staticfiles"]["BACKEND"]

# ── ARCHIVOS MULTIMEDIA (fotos y video subidos: /media/img, /media/videos) ──
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

if USAR_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": CLOUDINARY_API_KEY,
        "API_SECRET": CLOUDINARY_API_SECRET,
    }
    # Todo lo que se suba desde el admin (ImageField/FileField) se guarda en Cloudinary.
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── SEGURIDAD EN PRODUCCIÓN ──
# Solo se activan cuando DEBUG=False (o sea, cuando ya es un sitio público).
if not DEBUG:
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Dominios desde los que se permiten envíos de formularios (admin, contacto).
# Agrega aquí tu dominio real y/o el subdominio que te da tu hosting,
# por ejemplo: CSRF_TRUSTED_ORIGINS=https://guerreroscf.onrender.com
_csrf_origins = config("CSRF_TRUSTED_ORIGINS", default="")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]
