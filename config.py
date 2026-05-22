import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ustayease.db")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
