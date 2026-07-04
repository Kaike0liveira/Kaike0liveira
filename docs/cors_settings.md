# Configuração de CORS para React/Vercel consumindo Django/Railway

Instale os pacotes de API e CORS no `requirements.txt`:

```txt
Django>=5.0,<6.0
djangorestframework>=3.15,<4.0
django-cors-headers>=4.4,<5.0
```

No `settings.py`, adicione `corsheaders` antes dos apps locais e habilite o middleware do pacote antes do `CommonMiddleware`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "tactical_hub",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "https://seu-frontend.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://seu-frontend.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True
```

Use `CORS_ALLOWED_ORIGINS` com os domínios finais da Vercel. Evite `CORS_ALLOW_ALL_ORIGINS = True` em produção, porque isso abre a API para qualquer origem no navegador.
