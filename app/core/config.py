from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(".env"))

import os

DATABASE_URL = os.getenv("DATABASE_URL")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
APP_ENV = os.getenv("APP_ENV", "development")
