import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DBNAME = os.environ.get("DBNAME")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")