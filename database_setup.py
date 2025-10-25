# MongoDB Database Setup and Sample Data Generation

"""
This module sets up the MongoDB database, creates collections, and populates them with sample data
for the Smart CKD Health Management System.
"""

# Import required libraries
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
import uuid
from bson import ObjectId
from pymongo import MongoClient

print("Database setup system initialized successfully!")

# MongoDB Connection Setup
def connect_to_mongodb():
    """Connect to MongoDB and return database instance"""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ckd_health_management']
        
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        print(f"Database: {db.name}")
        return client, db
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None, None

def create_collections_and_indexes(db):
    """Create collections and indexes for better performance"""
    collections = ['patients', 'doctors', 'predictions', 'reports', 'recommendations', 'analytics']

    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection {collection_name} already exists")

    # Create indexes for better performance
    try:
        # Patients collection indexes
        db.patients.create_index("patient_id", unique=True)
        db.patients.create_index("personal_info.email", unique=True)
        
        # Doctors collection indexes
        db.doctors.create_index("doctor_id", unique=True)
        db.doctors.create_index("personal_info.email", unique=True)
        
        # Predictions collection indexes
        db.predictions.create_index("prediction_id", unique=True)
        db.predictions.create_index("patient_id")
        db.predictions.create_index("created_at")
        
        # Reports collection indexes
        db.reports.create_index("report_id", unique=True)
        db.reports.create_index("patient_id")
        
        # Recommendations collection indexes
        db.recommendations.create_index("recommendation_id", unique=True)
        db.recommendations.create_index("patient_id")
        
        # Analytics collection indexes
        db.analytics.create_index("date")
        
        print("All indexes created successfully!")
        
    except Exception as e:
        print(f"Error creating indexes: {e}")

def load_and_process_dataset():
    """Load and process the hospital dataset"""
    try:
        df = pd.read_csv('hospital real time.csv')
        print(f"Loaded dataset with {len(df)} records")
        print(f"Columns: {list(df.columns)}")

        # Display basic statistics
        print("\nDataset Info:")
        print(df.info())
        print("\nFirst 5 rows:")
        print(df.head())
        
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def create_sample_patients(df, db):
    """Create sample patient records from the dataset"""
    sample_patients = []

    for idx, row in df.head(50).iterrows():  # Take first 50 records as sample
        patient = {
            "patient_id": f"PAT_{str(uuid.uuid4())[:8]}",
            "personal_info": {
                "name": f"Patient {idx + 1}",
                "email": f"patient{idx + 1}@example.com",
                "phone": f"+91{random.randint(9000000000, 9999999999)}",
                "age": int(row['age']) if pd.notna(row['age']) else random.randint(25, 80),
                "gender": row['gender'] if pd.notna(row['gender']) else random.choice(['M', 'F']),
                "address": f"Address {idx + 1}, City, State",
                "emergency_contact": f"+91{random.randint(9000000000, 9999999999)}"
            },
            "health_history": {
                "blood_pressure": float(row['Blood_Pressure']) if pd.notna(row['Blood_Pressure']) else None,
                "sugar_level": float(row['Sugar_Level']) if pd.notna(row['Sugar_Level']) else None,
                "albumin": float(row['Albumin']) if pd.notna(row['Albumin']) else None,
                "serum_creatinine": float(row['Serum_Creatinine']) if pd.notna(row['Serum_Creatinine']) else None,
                "sodium": float(row['Sodium']) if pd.notna(row['Sodium']) else None,
                "potassium": float(row['Potassium']) if pd.notna(row['Potassium']) else None,
                "hemoglobin": float(row['Hemoglobin']) if pd.notna(row['Hemoglobin']) else None,
                "bun": float(row['BUN']) if pd.notna(row['BUN']) else None,
                "egfr": float(row['eGFR']) if pd.notna(row['eGFR']) else None,
                "acr": float(row['ACR']) if pd.notna(row['ACR']) else None,
                "ucr": float(row['UCR']) if pd.notna(row['UCR']) else None
            },
            "preferences": {
                "language": random.choice(['en', 'kn']),  # English or Kannada
                "theme": random.choice(['light', 'dark']),
                "notifications": random.choice([True, False])
            },
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365)),
            "updated_at": datetime.now()
        }
        sample_patients.append(patient)

    # Insert sample patients
    if sample_patients:
        result = db.patients.insert_many(sample_patients)
        print(f"Inserted {len(result.inserted_ids)} sample patients")
    else:
        print("No sample patients to insert")

def create_sample_doctors(db):
    """Create sample doctor records"""
    sample_doctors = [
        {
            "doctor_id": "DOC_001",
            "personal_info": {
                "name": "Dr. Rajesh Kumar",
                "email": "dr.rajesh@hospital.com",
                "phone": "+91-9876543210",
                "specialization": "Nephrology",
                "license_number": "MED123456",
                "hospital": "City General Hospital"
            },
            "patients_under_care": [],
            "created_at": datetime.now() - timedelta(days=30),
            "updated_at": datetime.now()
        },
        {
            "doctor_id": "DOC_002",
            "personal_info": {
                "name": "Dr. Priya Sharma",
                "email": "dr.priya@hospital.com",
                "phone": "+91-9876543211",
                "specialization": "Internal Medicine",
                "license_number": "MED123457",
                "hospital": "Metro Medical Center"
            },
            "patients_under_care": [],
            "created_at": datetime.now() - timedelta(days=25),
            "updated_at": datetime.now()
        },
        {
            "doctor_id": "DOC_003",
            "personal_info": {
                "name": "Dr. Amit Patel",
                "email": "dr.amit@hospital.com",
                "phone": "+91-9876543212",
                "specialization": "Cardiology",
                "license_number": "MED123458",
                "hospital": "Heart Care Institute"
            },
            "patients_under_care": [],
            "created_at": datetime.now() - timedelta(days=20),
            "updated_at": datetime.now()
        }
    ]

    # Insert sample doctors
    result = db.doctors.insert_many(sample_doctors)
    print(f"Inserted {len(result.inserted_ids)} sample doctors")

def create_sample_predictions(df, db):
    """Create sample prediction records"""
    sample_predictions = []

    # Get patient IDs from the database
    patient_ids = [patient['patient_id'] for patient in db.patients.find({}, {'patient_id': 1})]

    for idx, row in df.head(30).iterrows():  # Create predictions for first 30 records
        if idx < len(patient_ids):
            prediction = {
                "prediction_id": f"PRED_{str(uuid.uuid4())[:8]}",
                "patient_id": patient_ids[idx],
                "doctor_id": random.choice(["DOC_001", "DOC_002", "DOC_003"]),
                "input_data": {
                    "age": int(row['age']) if pd.notna(row['age']) else None,
                    "gender": row['gender'] if pd.notna(row['gender']) else None,
                    "blood_pressure": float(row['Blood_Pressure']) if pd.notna(row['Blood_Pressure']) else None,
                    "sugar_level": float(row['Sugar_Level']) if pd.notna(row['Sugar_Level']) else None,
                    "albumin": float(row['Albumin']) if pd.notna(row['Albumin']) else None,
                    "serum_creatinine": float(row['Serum_Creatinine']) if pd.notna(row['Serum_Creatinine']) else None,
                    "sodium": float(row['Sodium']) if pd.notna(row['Sodium']) else None,
                    "potassium": float(row['Potassium']) if pd.notna(row['Potassium']) else None,
                    "hemoglobin": float(row['Hemoglobin']) if pd.notna(row['Hemoglobin']) else None,
                    "bun": float(row['BUN']) if pd.notna(row['BUN']) else None,
                    "egfr": float(row['eGFR']) if pd.notna(row['eGFR']) else None,
                    "acr": float(row['ACR']) if pd.notna(row['ACR']) else None,
                    "ucr": float(row['UCR']) if pd.notna(row['UCR']) else None
                },
                "prediction_result": {
                    "ckd_binary": row['CKD_Binary'] == 'Yes',
                    "ckd_stage": row['CKD_Stage'] if pd.notna(row['CKD_Stage']) else 'No CKD',
                    "confidence_score": random.uniform(0.7, 0.99),
                    "risk_level": random.choice(['Low', 'Medium', 'High'])
                },
                "shap_values": {
                    "feature_importance": {
                        "egfr": random.uniform(0.1, 0.3),
                        "serum_creatinine": random.uniform(0.1, 0.25),
                        "age": random.uniform(0.05, 0.15),
                        "blood_pressure": random.uniform(0.05, 0.1)
                    }
                },
                "model_used": "Random Forest",
                "created_at": datetime.now() - timedelta(days=random.randint(1, 30))
            }
            sample_predictions.append(prediction)

    # Insert sample predictions
    if sample_predictions:
        result = db.predictions.insert_many(sample_predictions)
        print(f"Inserted {len(result.inserted_ids)} sample predictions")
    else:
        print("No sample predictions to insert")

def create_sample_recommendations(db):
    """Create sample recommendation records"""
    sample_recommendations = []

    # Get prediction data to create recommendations
    predictions = list(db.predictions.find({}, {'patient_id': 1, 'prediction_result': 1}))

    for pred in predictions[:20]:  # Create recommendations for first 20 predictions
        ckd_stage = pred['prediction_result']['ckd_stage']
        
        # Define diet plans based on CKD stage
        diet_plans = {
            'No CKD': {
                'breakfast': 'Oatmeal with fruits, low-fat milk',
                'lunch': 'Grilled chicken with brown rice and vegetables',
                'dinner': 'Fish with quinoa and salad',
                'snacks': 'Nuts, yogurt, fresh fruits'
            },
            'Stage 1': {
                'breakfast': 'Whole grain toast with avocado',
                'lunch': 'Lean protein with vegetables',
                'dinner': 'Baked fish with sweet potato',
                'snacks': 'Apple slices, unsalted nuts'
            },
            'Stage 2': {
                'breakfast': 'Low-sodium cereal with almond milk',
                'lunch': 'Grilled chicken salad',
                'dinner': 'Baked salmon with steamed vegetables',
                'snacks': 'Fresh berries, low-sodium crackers'
            },
            'Stage 3': {
                'breakfast': 'Low-phosphorus bread with jam',
                'lunch': 'Turkey sandwich on low-sodium bread',
                'dinner': 'Baked cod with rice',
                'snacks': 'Fresh fruits, low-sodium pretzels'
            },
            'Stage 4': {
                'breakfast': 'Low-potassium fruits with toast',
                'lunch': 'Chicken breast with white rice',
                'dinner': 'Baked white fish with pasta',
                'snacks': 'Low-potassium vegetables'
            },
            'Stage 5': {
                'breakfast': 'Low-phosphorus, low-potassium options',
                'lunch': 'Dialysis-friendly meal plan',
                'dinner': 'Renal diet approved foods',
                'snacks': 'Dialysis center approved snacks'
            }
        }
        
        # Define exercise plans based on CKD stage
        exercise_plans = {
            'No CKD': {
                'daily_activity': '30 minutes moderate exercise',
                'recommended_exercises': ['Walking', 'Swimming', 'Cycling', 'Yoga'],
                'frequency': '5-6 days per week',
                'intensity': 'Moderate'
            },
            'Stage 1': {
                'daily_activity': '25-30 minutes light to moderate exercise',
                'recommended_exercises': ['Walking', 'Swimming', 'Light yoga'],
                'frequency': '4-5 days per week',
                'intensity': 'Light to Moderate'
            },
            'Stage 2': {
                'daily_activity': '20-25 minutes light exercise',
                'recommended_exercises': ['Walking', 'Stretching', 'Gentle yoga'],
                'frequency': '3-4 days per week',
                'intensity': 'Light'
            },
            'Stage 3': {
                'daily_activity': '15-20 minutes gentle exercise',
                'recommended_exercises': ['Walking', 'Stretching', 'Breathing exercises'],
                'frequency': '3 days per week',
                'intensity': 'Very Light'
            },
            'Stage 4': {
                'daily_activity': '10-15 minutes very gentle movement',
                'recommended_exercises': ['Walking', 'Chair exercises', 'Breathing exercises'],
                'frequency': '2-3 days per week',
                'intensity': 'Very Light'
            },
            'Stage 5': {
                'daily_activity': '5-10 minutes gentle movement',
                'recommended_exercises': ['Chair exercises', 'Breathing exercises', 'Light stretching'],
                'frequency': 'As tolerated',
                'intensity': 'Minimal'
            }
        }
        
        recommendation = {
            "recommendation_id": f"REC_{str(uuid.uuid4())[:8]}",
            "patient_id": pred['patient_id'],
            "ckd_stage": ckd_stage,
            "diet_plan": diet_plans.get(ckd_stage, diet_plans['No CKD']),
            "exercise_plan": exercise_plans.get(ckd_stage, exercise_plans['No CKD']),
            "lifestyle_tips": [
                "Stay hydrated with appropriate fluid intake",
                "Monitor blood pressure regularly",
                "Follow prescribed medication schedule",
                "Maintain regular follow-ups with healthcare provider"
            ],
            "generated_by": "system",
            "created_at": datetime.now() - timedelta(days=random.randint(1, 15)),
            "updated_at": datetime.now()
        }
        sample_recommendations.append(recommendation)

    # Insert sample recommendations
    if sample_recommendations:
        result = db.recommendations.insert_many(sample_recommendations)
        print(f"Inserted {len(result.inserted_ids)} sample recommendations")
    else:
        print("No sample recommendations to insert")

def create_analytics_data(db):
    """Create analytics data"""
    total_patients = db.patients.count_documents({})
    ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": True})
    non_ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": False})
    total_predictions = db.predictions.count_documents({})

    # Calculate stage distribution
    stage_pipeline = [
        {"$group": {"_id": "$prediction_result.ckd_stage", "count": {"$sum": 1}}}
    ]
    stage_distribution = {}
    for stage_data in db.predictions.aggregate(stage_pipeline):
        stage_distribution[stage_data['_id']] = stage_data['count']

    # Calculate average confidence score
    confidence_pipeline = [
        {"$group": {"_id": None, "avg_confidence": {"$avg": "$prediction_result.confidence_score"}}}
    ]
    avg_confidence_result = list(db.predictions.aggregate(confidence_pipeline))
    avg_confidence = avg_confidence_result[0]['avg_confidence'] if avg_confidence_result else 0

    analytics_data = {
        "date": datetime.now(),
        "total_patients": total_patients,
        "ckd_patients": ckd_patients,
        "non_ckd_patients": non_ckd_patients,
        "stage_distribution": stage_distribution,
        "model_accuracy": 0.9808,  # From our Random Forest model
        "total_predictions": total_predictions,
        "average_risk_score": avg_confidence
    }

    # Insert analytics data
    result = db.analytics.insert_one(analytics_data)
    print(f"Inserted analytics data with ID: {result.inserted_id}")
    print(f"Total patients: {total_patients}")
    print(f"CKD patients: {ckd_patients}")
    print(f"Non-CKD patients: {non_ckd_patients}")
    print(f"Stage distribution: {stage_distribution}")

def verify_database_setup(db):
    """Verify database setup and display summary"""
    print("=== MongoDB Database Setup Complete ===\n")

    print("Collection Statistics:")
    collections = ['patients', 'doctors', 'predictions', 'reports', 'recommendations', 'analytics']
    for collection_name in collections:
        count = db[collection_name].count_documents({})
        print(f"{collection_name}: {count} documents")

    print("\nSample Data Verification:")
    sample_patient = db.patients.find_one({}, {"patient_id": 1, "personal_info.name": 1, "personal_info.age": 1})
    print(sample_patient)

    print("\nSample Doctor:")
    sample_doctor = db.doctors.find_one({}, {"doctor_id": 1, "personal_info.name": 1, "personal_info.specialization": 1})
    print(sample_doctor)

    print("\nSample Prediction:")
    sample_prediction = db.predictions.find_one({}, {"prediction_id": 1, "patient_id": 1, "prediction_result.ckd_binary": 1, "prediction_result.ckd_stage": 1})
    print(sample_prediction)

    print("\nDatabase setup completed successfully!")
    print("Ready for Flask application integration.")

def main():
    """Main function to set up the database"""
    print("=== Smart CKD Health Management - Database Setup ===\n")
    
    # Connect to MongoDB
    client, db = connect_to_mongodb()
    if db is None:
        print("Failed to connect to MongoDB. Please ensure MongoDB is running on localhost:27017")
        return
    
    # Create collections and indexes
    print("\n1. Creating collections and indexes...")
    create_collections_and_indexes(db)
    
    # Load dataset
    print("\n2. Loading and processing dataset...")
    df = load_and_process_dataset()
    if df is None:
        print("Failed to load dataset. Please ensure 'hospital real time.csv' exists.")
        return
    
    # Create sample data
    print("\n3. Creating sample patients...")
    create_sample_patients(df, db)
    
    print("\n4. Creating sample doctors...")
    create_sample_doctors(db)
    
    print("\n5. Creating sample predictions...")
    create_sample_predictions(df, db)
    
    print("\n6. Creating sample recommendations...")
    create_sample_recommendations(db)
    
    print("\n7. Creating analytics data...")
    create_analytics_data(db)
    
    # Verify setup
    print("\n8. Verifying database setup...")
    verify_database_setup(db)
    
    print("\n=== Database Setup Complete ===")

if __name__ == "__main__":
    main()
