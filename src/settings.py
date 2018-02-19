import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

DB_NAME = os.environ.get("DB_NAME")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
TABLE = os.environ.get("TABLE")