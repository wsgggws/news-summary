import os

from dotenv import load_dotenv

env_file = ".env.test" if os.getenv("CI") == "true" else ".env"

load_dotenv(env_file)


DATABASE_URL = os.getenv("DATABASE_URL") or ""
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or ""

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60
