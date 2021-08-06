from .base import *

SECRET_KEY = (
    "django-insecure-4^%s&n9v0#wlc%cf)=%vf+2l0aqq^92365254579(ac=13ng9"
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "api.postcodes.io"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "TEST": {"NAME": os.environ.get("TEST_DB_NAME")},
    }
}
