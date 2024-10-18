from pymongo import MongoClient

def get_db():
    # Use the provided MongoDB Atlas connection string
    client = MongoClient("mongodb+srv://pavan:charan12@microblog.afyjl.mongodb.net/?retryWrites=true&w=majority&appName=microblog")
    db = client['medication_adherence']  # Ensure this database exists or create it
    return db
