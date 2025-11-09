from typing import Any
import os


def get_logging_config(
    log_level: str = 'INFO',
    enable_file_logging: bool = False,
    log_file: str = 'logs/app.log',
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> dict[str, Any]:
    if enable_file_logging:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter_name = 'detailed'

    config: dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | [%(process)d] | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | %(filename)s:%(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': formatter_name,
                'stream': 'ext://sys.stdout',
                'level': log_level
            },
        },
        'root': {
            'level': log_level,
            'handlers': ['console']
        },
        'loggers': {
            'uvicorn': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': False
            },
            'uvicorn.error': {
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.access': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': False
            },
            'sqlalchemy.engine': {
                'level': 'WARNING',
                'propagate': False
            },
            'fastapi': {
                'level': 'INFO',
                'propagate': False
            },
            'app': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            }
        }
    }

    if enable_file_logging:
        config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': formatter_name,
            'filename': log_file,
            'maxBytes': max_file_size,
            'backupCount': backup_count,
            'encoding': 'utf-8',
            'level': log_level
        }
        config['root']['handlers'].append('file')
        for logger in ['uvicorn', 'uvicorn.access', 'app']:
            if logger in config['loggers']:
                config['loggers'][logger]['handlers'].append('file')
    return config
