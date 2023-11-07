logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s"
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": 'app.log',
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "file"
        ],
        "propagate": True
    }
}