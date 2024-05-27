from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
DEV = os.getenv('DEV')
DB = os.getenv('DB')
ISDEV = os.getenv('ISDEV')