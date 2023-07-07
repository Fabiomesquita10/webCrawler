from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient("mongodb://localhost:27017/")
    try:
        client.server_info()
        # print("Connected to MongoDB successfully!")
    except Exception as e:
        print("Failed to connect to MongoDB: " + e)
    db = client["priceChecker"]
    return db

def get_collection(collection_name: str):
    db = get_mongo_client()
    collection = db[collection_name]
    return collection


