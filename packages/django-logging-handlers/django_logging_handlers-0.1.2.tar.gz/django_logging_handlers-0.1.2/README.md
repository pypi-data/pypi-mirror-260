# Django logging handlers

Django logging handlers is a collection of handlers for logging messages to various services, such as Telegram, Slack, Discord, and more.

![Static Badge](https://img.shields.io/badge/Code_style-Google-blue)
![Static Badge](https://img.shields.io/badge/Commit_style-Conventional-fe5196)

## Quick start

1. Install via pip

```bash
pip install django-logging-handlers
```

2. Add `django-logging-handlers` to your INSTALLED_APPS setting like this

```python
INSTALLED_APPS = [
    ...
    'django_logging_handlers',
]
```

3. Register Logging

```python
LOGGING = {
    ...
    "handlers": {
        ...
        "telegram": {
            "level": "ERROR",
            "class": "django_logging_handlers.handlers.TelegramHandler",
            "token": "<telegram bot token>",
            "chat": "<chat id>",
            "message": "",             # optional: if you want to add a message together
                                       #           with the traceback
            "file_name": PROJECT_NAME, # optional: if you want to edit the file name,
                                       #           defaults to "traceback.html"
        },
    },
    "loggers": {
        "django.request": {
            "handlers": [..., "telegram"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
```

## Live Features

- Telegram

## Planned features

- Slack
- Discord
