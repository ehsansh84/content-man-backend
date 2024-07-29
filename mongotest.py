import pymongo

client = pymongo.MongoClient("mongodb://mongodb:270i17")  # Replace with your MongoDB URI
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


