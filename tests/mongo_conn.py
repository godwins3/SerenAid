from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

def test_mongodb_connection(uri):
    try:
        # Create a MongoClient instance with the provided URI
        client = MongoClient(uri)
        
        # Attempt to connect to the server
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        
        # Close the client connection
        client.close()
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your MongoDB connection URI
    uri = os.getenv('MONGO_URI')
    test_mongodb_connection(uri)
