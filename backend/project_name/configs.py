from os import environ as env

from dotenv import load_dotenv

load_dotenv()

WEB_URL = env.get("WEB_URL")

project_name_HOST = env.get("project_name_HOST")
project_name_PORT = int(env.get("project_name_PORT"))

HASH_SECRET_KEY = env.get("HASH_SECRET_KEY")
HASH_ALGORITHM = env.get("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

POSTGRES_USER = env.get("POSTGRES_USER")
POSTGRES_PASSWORD = env.get("POSTGRES_PASSWORD")
POSTGRES_HOST = env.get("POSTGRES_HOST")
POSTGRES_PORT = int(env.get("POSTGRES_PORT"))
POSTGRES_DB = env.get("POSTGRES_DB")

POLYGON_API_KEY = env.get("POLYGON_API_KEY")

SUPPORT_EMAIL = env.get("SUPPORT_EMAIL")
SUPPORT_EMAIL_APP_PASSWORD = env.get("SUPPORT_EMAIL_APP_PASSWORD")
