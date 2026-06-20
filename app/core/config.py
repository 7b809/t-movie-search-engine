import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL")
POSTER_BASE_URL = os.getenv("POSTER_BASE_URL")

# MongoDB connection string
MONGO_URL = os.getenv("MONGO_URL")