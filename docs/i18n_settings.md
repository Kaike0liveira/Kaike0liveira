# Configuração de internacionalização do Django

Para permitir que o Django detecte automaticamente o idioma enviado pelo frontend React no cabeçalho HTTP `Accept-Language`, habilite o `LocaleMiddleware` no `settings.py` logo depois do `SessionMiddleware` e antes do `CommonMiddleware`.

```python
from django.utils.translation import gettext_lazy as _

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LANGUAGE_CODE = "pt-br"

LANGUAGES = (
    ("pt-br", _("Português do Brasil")),
    ("en", _("English")),
)

USE_I18N = True
```

Com essa configuração, requisições com `Accept-Language: en` recebem traduções em inglês quando disponíveis; sem cabeçalho, o padrão permanece `pt-br`.
