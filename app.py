from flask import Flask, render_template, request, redirect, url_for, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Use the provided MongoDB Atlas connection string
client = MongoClient("mongodb+srv://pavan:charan12@microblog.afyjl.mongodb.net/?retryWrites=true&w=majority&appName=microblog")
db = client['medication_adherence']
patients_collection = db.patients

@app.route('/')
def root():
    # Redirect to the welcome page
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/patients')
def index():
    patients = patients_collection.find().limit(30)
    return render_template('index.html', patients=patients)

@app.route('/patients/<patient_id>')
def patient_profile(patient_id):
    patient = patients_collection.find_one({'_id': ObjectId(patient_id)})
    if patient:
        # Prepare data for the pie chart
        taken = sum(1 for record in patient['adherence'] if record['status'] == "Taken")
        not_taken = sum(1 for record in patient['adherence'] if record['status'] == "Not Taken")
        
        return render_template('profile.html', patient=patient, taken=taken, not_taken=not_taken)
    else:
        return "Patient not found", 404

# Fetch medication data for a specific patient for the selected date
@app.route('/patients/<patient_id>/medication', methods=['GET'])
def patient_medication_overview(patient_id):
    patient = patients_collection.find_one({'_id': ObjectId(patient_id)})
    selected_date_str = request.args.get('date')

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y")
        medication_overview = [
            record for record in patient['adherence'] if record['date'].strftime("%d-%m-%Y") == selected_date_str
        ]
    else:
        # Fetch all medication adherence records for the last month
        medication_overview = [
            record for record in patient['adherence'] if record['date'] >= (datetime.now() - timedelta(days=30))
        ]

    if medication_overview:
        taken = sum(1 for record in medication_overview if record['status'] == "Taken")
        not_taken = sum(1 for record in medication_overview if record['status'] == "Not Taken")
        return jsonify({'taken': taken, 'not_taken': not_taken})
    else:
        return jsonify({"error": "No medication records found for this date"}), 404

if __name__ == '__main__':
    app.run(debug=True)
