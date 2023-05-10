import os

from dotenv import load_dotenv

load_dotenv()

# Database configs
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Database configs for tests
DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")

# Auth and Manager secrets
SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_MANAGER = os.environ.get("SECRET_MANAGER")

# Mailing configs
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
