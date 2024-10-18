from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Use the provided MongoDB Atlas connection string
client = MongoClient("mongodb+srv://pavan:charan12@microblog.afyjl.mongodb.net/?retryWrites=true&w=majority&appName=microblog")
db = client['medication_adherence']
patients_collection = db.patients

# Clear existing data
patients_collection.delete_many({})

# Generate dummy data for 30 patients
dummy_patients = []
for i in range(1, 31):
    patient = {
        "name": f"Patient {i}",
        "age": random.randint(20, 80),
        "gender": "Male" if i % 2 == 0 else "Female",
        "contact": f"12345678{i}",
        "address": f"{i} Pine Street",
        "medication": [{"name": f"Medicine {i}", "dosage": f"{random.randint(10, 100)}mg", "frequency": "Once daily"}],
        "adherence": [
            {"date": datetime.now() - timedelta(days=random.randint(1, 30)), "status": random.choice(["Taken", "Not Taken"])}
            for _ in range(30)  # Generating adherence for 30 days
        ],
        "pinned": i > 15  # Pin patients 16-30
    }
    dummy_patients.append(patient)

# Insert the dummy patients into MongoDB
patients_collection.insert_many(dummy_patients)
print("Database seeded with 30 dummy patients.")
