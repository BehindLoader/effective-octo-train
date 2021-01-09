import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project settings."""

    UVICORN_RELOAD: bool = False
    UVICORN_DEBUG: bool = False
    UVICORN_LOG_LEVEL: str = 'debug'

    TELEGRAM_BOT_TOKEN: str

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'uvicorn.error': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/error.log',
                'formatter': 'standard',
                'maxBytes': 1024 ** 3 * 10,
                'backupCount': 10,
            },
            'uvicorn.access': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/access.log',
                'formatter': 'standard',
                'maxBytes': 1024 ** 3 * 10,
                'backupCount': 10,
            },
            'TelegramWebHook': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/webhook.log',
                'formatter': 'standard',
                'maxBytes': 1024 ** 3 * 10,
                'backupCount': 10,
            },
            'TelegramClient': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/telegram_api_error.log',
                'formatter': 'standard',
                'maxBytes': 1024 ** 3 * 10,
                'backupCount': 10,
            }
        },
        'loggers': {
            '*': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'uvicorn.access': {
                'handlers': ['uvicorn.access'],
                'level': 'INFO',
                'propagate': True,
            },
            'uvicorn.error': {
                'handlers': ['uvicorn.error'],
                'level': 'WARNING',
                'propagate': True,
            },
            'TelegramWebHook': {
                'handlers': ['TelegramWebHook'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'TelegramClient': {
                'handlers': ['TelegramClient'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }


settings = Settings()
