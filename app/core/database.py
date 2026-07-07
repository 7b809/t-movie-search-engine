from pymongo import MongoClient
from app.core.config import MONGO_URL

# Initialize Client Connection
client = MongoClient(MONGO_URL)

# Access database context
db = client["flicks_search_engine_db"]
daily_watch_collection = db["daily_watch"] # Add this line

# Collection assignments
favorites_collection = db["favorites"]