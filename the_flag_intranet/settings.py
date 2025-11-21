# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Lade Umgebungsvariablen (wie den Secret Key) aus einer .env-Datei
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SICHERHEIT: Dies wird später auf Render gesetzt
SECRET_KEY = os.getenv('SECRET_KEY', 'default-insecure-key-for-development')

# WICHTIG: Erlaubt nur Zugriff von der offiziellen Domain (später bei Render)
ALLOWED_HOSTS = ['*'] # * sollte später auf die Render-URL geändert werden

# Installierte Django-Apps
INSTALLED_APPS = [
    # Wichtig: Wir müssen unseren eigenen Mitarbeiter als User-Modell definieren
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'intranet_app', # Unsere Intranet-Anwendung
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'the_flag_intranet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'the_flag_intranet.wsgi.application'

# Datenbank (wird später von Render konfiguriert)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Platzhalter
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Unser Custom User Model
AUTH_USER_MODEL = 'intranet_app.Mitarbeiter'

# Passwort-Validierung, etc. (Kann der Programmierer später anpassen)
AUTH_PASSWORD_VALIDATORS = [
    # ...
]

# Zeitzone (Deutschland)
LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_TZ = True

# Statische Dateien (CSS, JS, Bilder)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Konfiguration für E-Mails (muss später eingerichtet werden)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
# -----------------------------------------------------------
# AUTHENTIFIZIERUNG UND UMLEITUNGEN
# -----------------------------------------------------------

# Wo soll der User nach dem Login hingeleitet werden? -> Zum Dashboard
LOGIN_REDIRECT_URL = '/' 

# Wo soll der User nach dem Logout hingeleitet werden? -> Zur Startseite (die Login anzeigt)
LOGOUT_REDIRECT_URL = '/'
