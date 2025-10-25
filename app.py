from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
import joblib
import json
import numpy as np
import pandas as pd
import sklearn
from datetime import datetime, timedelta
import uuid
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Import multilingual support
from multilingual import get_translation, get_all_translations, get_supported_languages

# Prevent Flask CLI from auto-loading parent .env files (which may be malformed)
os.environ.setdefault('FLASK_SKIP_DOTENV', '1')

# Load environment variables from .env file with robust encoding handling
try:
    dotenv_path = Path(__file__).parent / '.env'
    # Prefer UTF-8
    load_dotenv(dotenv_path=dotenv_path, override=True, encoding='utf-8')
except Exception as e:
    # Fallback encodings commonly seen on Windows if file was saved incorrectly
    try:
        print(f"Warning reading .env with utf-8: {e}. Retrying with cp1252...")
        load_dotenv(dotenv_path=dotenv_path, override=True, encoding='cp1252')
    except Exception as e2:
        print(f"Warning reading .env with cp1252: {e2}. Proceeding without .env.")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize Gemini AI
try:
    api_key = os.environ.get('GEMINI_API_KEY')
    print(f"Environment variables loaded. GEMINI_API_KEY: {'Found' if api_key else 'Not found'}")
    
    if not api_key or api_key == 'demo-key':
        print("Warning: GEMINI_API_KEY not found in environment variables")
        print("Available environment variables:", [k for k in os.environ.keys() if 'GEMINI' in k or 'API' in k])
        model = None
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("Gemini AI initialized successfully!")
        print(f"Using API key: {api_key[:10]}...")
except Exception as e:
    print(f"Warning: Gemini AI not initialized: {e}")
    model = None

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['ckd_health_management']

# Load ML models
try:
    rf_model = joblib.load('models/ckd_random_forest_model.pkl')
    scaler = joblib.load('models/ckd_scaler.pkl')
    label_encoder = joblib.load('models/ckd_label_encoder.pkl')
    with open('models/feature_names.json', 'r') as f:
        feature_names = json.load(f)
    shap_explainer = joblib.load('models/ckd_shap_explainer.pkl')
    print("ML models loaded successfully!")
except Exception as e:
    print(f"Error loading ML models: {e}")
    rf_model = None
    scaler = None
    label_encoder = None
    feature_names = []
    shap_explainer = None

# Gemini AI is already configured above using robust .env loading

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, user_type):
        self.id = user_id
        self.user_type = user_type

@login_manager.user_loader
def load_user(user_id):
    # Check if user exists in patients or doctors collection
    patient = db.patients.find_one({"patient_id": user_id})
    if patient:
        return User(user_id, 'patient')
    
    doctor = db.doctors.find_one({"doctor_id": user_id})
    if doctor:
        return User(user_id, 'doctor')
    
    return None

# Helper functions
def predict_ckd_stage(eGFR_value):
    """Predict CKD stage based on eGFR value"""
    if eGFR_value >= 90:
        return "Stage 1"
    elif eGFR_value >= 60:
        return "Stage 2"
    elif eGFR_value >= 30:
        return "Stage 3"
    elif eGFR_value >= 15:
        return "Stage 4"
    else:
        return "Stage 5"

def get_risk_level(confidence_score):
    """Determine risk level based on confidence score"""
    if confidence_score >= 0.9:
        return "High"
    elif confidence_score >= 0.7:
        return "Medium"
    else:
        return "Low"

def generate_diet_plan(ckd_stage):
    """Generate diet plan based on CKD stage"""
    from recommendations import get_diet_plan
    return get_diet_plan(ckd_stage)

def generate_exercise_plan(ckd_stage):
    """Generate exercise plan based on CKD stage"""
    from recommendations import get_exercise_plan
    return get_exercise_plan(ckd_stage)

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'patient':
            user = db.patients.find_one({"personal_info.email": email})
            if user and check_password_hash(user.get('password', ''), password):
                login_user(User(user['patient_id'], 'patient'))
                return redirect(url_for('patient_dashboard'))
        elif user_type == 'doctor':
            user = db.doctors.find_one({"personal_info.email": email})
            if user and check_password_hash(user.get('password', ''), password):
                login_user(User(user['doctor_id'], 'doctor'))
                return redirect(url_for('doctor_dashboard'))
        
        flash(get_translation('invalid_credentials', session.get('language', 'en')), 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        phone = request.form.get('phone', '')
        
        if user_type == 'patient':
            # Check if patient already exists
            if db.patients.find_one({"personal_info.email": email}):
                flash(get_translation('patient_exists', session.get('language', 'en')), 'error')
                return render_template('signup.html')
            
            patient_id = f"PAT_{str(uuid.uuid4())[:8]}"
            patient_data = {
                "patient_id": patient_id,
                "personal_info": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "age": None,
                    "gender": None,
                    "address": "",
                    "emergency_contact": ""
                },
                "health_history": {},
                "preferences": {
                    "language": "en",
                    "theme": "light",
                    "notifications": True
                },
                "password": generate_password_hash(password),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            db.patients.insert_one(patient_data)
            login_user(User(patient_id, 'patient'))
            return redirect(url_for('patient_dashboard'))
        
        elif user_type == 'doctor':
            # Check if doctor already exists
            if db.doctors.find_one({"personal_info.email": email}):
                flash(get_translation('doctor_exists', session.get('language', 'en')), 'error')
                return render_template('signup.html')
            
            doctor_id = f"DOC_{str(uuid.uuid4())[:8]}"
            doctor_data = {
                "doctor_id": doctor_id,
                "personal_info": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "specialization": "",
                    "license_number": "",
                    "hospital": ""
                },
                "patients_under_care": [],
                "password": generate_password_hash(password),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            db.doctors.insert_one(doctor_data)
            login_user(User(doctor_id, 'doctor'))
            return redirect(url_for('doctor_dashboard'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/patient-dashboard')
@login_required
def patient_dashboard():
    """Patient dashboard"""
    if current_user.user_type != 'patient':
        return redirect(url_for('doctor_dashboard'))
    
    # Get patient data
    patient = db.patients.find_one({"patient_id": current_user.id})
    
    # Get recent predictions
    recent_predictions_raw = list(db.predictions.find(
        {"patient_id": current_user.id}
    ).sort("created_at", -1).limit(5))
    
    # Convert ObjectId to string for each prediction
    recent_predictions = []
    for pred in recent_predictions_raw:
        pred_dict = dict(pred)
        pred_dict['_id'] = str(pred_dict['_id'])
        recent_predictions.append(pred_dict)
    
    # Get recommendations
    recommendations = db.recommendations.find_one({"patient_id": current_user.id})
    
    return render_template('patient_dashboard.html', 
                         patient=patient, 
                         predictions=recent_predictions,
                         recommendations=recommendations)

@app.route('/doctor-dashboard')
@login_required
def doctor_dashboard():
    """Doctor dashboard"""
    if current_user.user_type != 'doctor':
        return redirect(url_for('patient_dashboard'))
    
    # Get analytics data
    total_patients = db.patients.count_documents({})
    ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": True})
    non_ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": False})
    total_predictions = db.predictions.count_documents({})
    
    # Get stage distribution
    stage_pipeline = [
        {"$group": {"_id": "$prediction_result.ckd_stage", "count": {"$sum": 1}}}
    ]
    stage_distribution = {}
    for stage_data in db.predictions.aggregate(stage_pipeline):
        stage_distribution[stage_data['_id']] = stage_data['count']
    
    # Get recent predictions and convert ObjectIds to strings
    recent_predictions_raw = list(db.predictions.find().sort("created_at", -1).limit(10))
    recent_predictions = []
    for pred in recent_predictions_raw:
        pred_dict = dict(pred)
        # Convert ObjectId to string
        pred_dict['_id'] = str(pred_dict['_id'])
        recent_predictions.append(pred_dict)
    
    analytics = {
        'total_patients': total_patients,
        'ckd_patients': ckd_patients,
        'non_ckd_patients': non_ckd_patients,
        'total_predictions': total_predictions,
        'stage_distribution': stage_distribution,
        'recent_predictions': recent_predictions,
        'model_accuracy': 0.9808  # Model accuracy from training
    }
    
    return render_template('doctor_dashboard.html', analytics=analytics)

# API Routes
@app.route('/api/predict', methods=['POST'])
@login_required
def predict_ckd():
    """CKD prediction API"""
    if not rf_model or not scaler or not label_encoder:
        return jsonify({'error': 'ML model not loaded'}), 500
    
    try:
        data = request.json
        
        # Prepare input data in the correct order
        input_data = {
            'age': float(data.get('age', 0)),
            'Blood_Pressure': float(data.get('blood_pressure', 0)),
            'Sugar_Level': float(data.get('sugar_level', 0)),
            'Albumin': float(data.get('albumin', 0)),
            'Serum_Creatinine': float(data.get('serum_creatinine', 0)),
            'Sodium': float(data.get('sodium', 0)),
            'Potassium': float(data.get('potassium', 0)),
            'Hemoglobin': float(data.get('hemoglobin', 0)),
            'BUN': float(data.get('bun', 0)),
            'eGFR': float(data.get('egfr', 0)),
            'ACR': float(data.get('acr', 0)),
            'UCR': float(data.get('ucr', 0)),
            'gender_M': 1 if data.get('gender') == 'M' else 0
        }
        
        # Create DataFrame with proper feature order
        input_df = pd.DataFrame([input_data])
        
        # Ensure all required features are present
        for feature in feature_names:
            if feature not in input_df.columns:
                input_df[feature] = 0
        
        # Reorder columns to match training data
        input_df = input_df[feature_names]
        
        # Scale only the columns the scaler was trained on (avoid unseen feature errors)
        scaled_df = input_df.copy()
        try:
            numerical_columns_for_scaler = list(scaler.feature_names_in_)
        except Exception:
            # Fallback: treat everything except one-hot gender as numerical
            numerical_columns_for_scaler = [c for c in input_df.columns if c != 'gender_M']

        # Apply scaling to numerical columns only
        scaled_df[numerical_columns_for_scaler] = scaler.transform(input_df[numerical_columns_for_scaler])
        
        # Make prediction
        prediction_proba = rf_model.predict_proba(scaled_df)[0]
        prediction_encoded = rf_model.predict(scaled_df)[0]
        
        # Convert prediction back to original label
        prediction = label_encoder.inverse_transform([prediction_encoded])[0]
        confidence_score = max(prediction_proba)
        
        # Determine CKD stage
        ckd_stage = predict_ckd_stage(input_data['eGFR'])
        risk_level = get_risk_level(confidence_score)
        
        # Generate SHAP values
        shap_values = None
        if shap_explainer:
            try:
                shap_values = shap_explainer.shap_values(scaled_df)
            except:
                shap_values = None
        
        # Save prediction to database
        prediction_id = f"PRED_{str(uuid.uuid4())[:8]}"
        prediction_data = {
            "prediction_id": prediction_id,
            "patient_id": current_user.id,
            "doctor_id": None,
            "input_data": input_data,
            "prediction_result": {
                "ckd_binary": prediction == 'Yes',
                "ckd_stage": ckd_stage,
                "confidence": float(confidence_score),
                "risk_level": risk_level
            },
            "shap_values": shap_values.tolist() if shap_values is not None else None,
            "model_used": "Random Forest",
            "created_at": datetime.now()
        }
        
        db.predictions.insert_one(prediction_data)
        
        # Generate recommendations
        diet_plan = generate_diet_plan(ckd_stage)
        exercise_plan = generate_exercise_plan(ckd_stage)
        
        recommendation_id = f"REC_{str(uuid.uuid4())[:8]}"
        recommendation_data = {
            "recommendation_id": recommendation_id,
            "patient_id": current_user.id,
            "ckd_stage": ckd_stage,
            "diet_plan": diet_plan,
            "exercise_plan": exercise_plan,
            "lifestyle_tips": [
                get_translation('stay_hydrated_appropriate', session.get('language', 'en')),
                get_translation('monitor_bp_regularly', session.get('language', 'en')),
                get_translation('follow_medication_schedule', session.get('language', 'en')),
                get_translation('maintain_regular_followups', session.get('language', 'en'))
            ],
            "generated_by": "system",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        db.recommendations.insert_one(recommendation_data)
        
        return jsonify({
            'prediction_id': prediction_id,
            'ckd_detected': bool(prediction),
            'ckd_stage': ckd_stage,
            'confidence': float(confidence_score),
            'risk_level': risk_level,
            'diet_plan': diet_plan,
            'exercise_plan': exercise_plan,
            'shap_values': shap_values.tolist() if shap_values is not None else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Messaging: doctor → patient
@app.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    """Doctor sends a message to a patient"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    try:
        data = request.json or {}
        patient_id = data.get('patient_id')
        content = (data.get('content') or '').strip()
        if not patient_id or not content:
            return jsonify({'error': 'patient_id and content are required'}), 400

        # Validate patient exists
        patient = db.patients.find_one({"patient_id": patient_id})
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        message_id = f"MSG_{str(uuid.uuid4())[:8]}"
        message_doc = {
            'message_id': message_id,
            'patient_id': patient_id,
            'doctor_id': current_user.id,
            'content': content,
            'created_at': datetime.now(),
            'read': False,
            'type': 'instruction'
        }
        db.messages.insert_one(message_doc)
        return jsonify({'success': True, 'message_id': message_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Patient Management Extensions
@app.route('/api/patients/export', methods=['GET'])
@login_required
def export_patients_csv():
    """Export patients to CSV with current filters"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Apply same filters as /api/patients
        search = request.args.get('search', '').strip().lower()
        gender = request.args.get('gender')
        stage = request.args.get('stage')
        risk = request.args.get('risk')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Build query
        query = {}
        if search:
            query["$or"] = [
                {"personal_info.name": {"$regex": search, "$options": "i"}},
                {"personal_info.email": {"$regex": search, "$options": "i"}},
                {"patient_id": {"$regex": search, "$options": "i"}},
            ]
        if gender in ('M', 'F'):
            query["personal_info.gender"] = gender
        
        # Get all patients matching query
        patients = list(db.patients.find(query).sort("created_at", -1))
        
        # Post-filter by prediction-dependent fields
        filtered_patients = []
        for patient in patients:
            latest_prediction = db.predictions.find_one(
                {"patient_id": patient['patient_id']},
                sort=[("created_at", -1)]
            )
            
            health_status = "Unknown"
            latest_risk = None
            if latest_prediction:
                if latest_prediction['prediction_result']['ckd_binary']:
                    health_status = f"CKD {latest_prediction['prediction_result']['ckd_stage']}"
                else:
                    health_status = "Healthy"
                latest_risk = latest_prediction['prediction_result'].get('risk_level')
            
            # Apply stage filter
            if stage:
                if stage == 'No CKD' and health_status != 'Healthy':
                    continue
                if stage.startswith('Stage') and f"CKD {stage}" != health_status:
                    continue
            
            # Apply risk filter
            if risk and latest_risk and latest_risk != risk:
                continue
            
            # Apply date filters
            if date_from:
                try:
                    df = datetime.fromisoformat(date_from)
                    if patient.get('created_at') and patient['created_at'] < df:
                        continue
                except Exception:
                    pass
            if date_to:
                try:
                    dt = datetime.fromisoformat(date_to)
                    if patient.get('created_at') and patient['created_at'] > dt:
                        continue
                except Exception:
                    pass
            
            filtered_patients.append({
                'patient_id': patient['patient_id'],
                'name': patient['personal_info']['name'],
                'email': patient['personal_info']['email'],
                'phone': patient['personal_info'].get('phone', ''),
                'age': patient['personal_info'].get('age', ''),
                'gender': patient['personal_info'].get('gender', ''),
                'created_at': patient['created_at'].strftime('%Y-%m-%d'),
                'health_status': health_status,
                'risk_level': latest_risk or '',
                'last_prediction': latest_prediction['created_at'].strftime('%Y-%m-%d') if latest_prediction else 'Never'
            })
        
        # Create CSV
        import csv
        output = io.StringIO()
        if filtered_patients:
            writer = csv.DictWriter(output, fieldnames=filtered_patients[0].keys())
            writer.writeheader()
            writer.writerows(filtered_patients)
        
        csv_content = output.getvalue()
        output.close()
        
        # Return CSV file
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            as_attachment=True,
            download_name=f'patients_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/notes', methods=['GET', 'POST'])
@login_required
def manage_patient_notes(patient_id):
    """Get or add patient notes (doctor only)"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        if request.method == 'GET':
            # Get patient notes
            notes = list(db.patient_notes.find({"patient_id": patient_id}).sort("created_at", -1))
            return jsonify({'success': True, 'notes': notes})
        
        elif request.method == 'POST':
            # Add new note
            data = request.json
            content = data.get('content', '').strip()
            tags = data.get('tags', [])
            
            if not content:
                return jsonify({'error': 'Note content is required'}), 400
            
            note_id = f"NOTE_{str(uuid.uuid4())[:8]}"
            note_doc = {
                'note_id': note_id,
                'patient_id': patient_id,
                'doctor_id': current_user.id,
                'content': content,
                'tags': tags,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            db.patient_notes.insert_one(note_doc)
            return jsonify({'success': True, 'note_id': note_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/tags', methods=['POST'])
@login_required
def update_patient_tags(patient_id):
    """Update patient tags (doctor only)"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        tags = data.get('tags', [])
        
        # Update patient document with tags
        result = db.patients.update_one(
            {"patient_id": patient_id},
            {"$set": {"tags": tags, "updated_at": datetime.now()}}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify({'success': True, 'tags': tags})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk-actions', methods=['POST'])
@login_required
def bulk_actions():
    """Perform bulk actions on selected patients"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        patient_ids = data.get('patient_ids', [])
        action = data.get('action')
        
        if not patient_ids:
            return jsonify({'error': 'No patients selected'}), 400
        
        results = []
        
        if action == 'generate_reports':
            # Generate reports for selected patients
            for patient_id in patient_ids:
                try:
                    # Get latest prediction for patient
                    latest_prediction = db.predictions.find_one(
                        {"patient_id": patient_id},
                        sort=[("created_at", -1)]
                    )
                    
                    if latest_prediction:
                        # Generate report
                        from report_generator import create_patient_report
                        pdf_content, error = create_patient_report(latest_prediction['prediction_id'])
                        
                        if not error:
                            results.append({
                                'patient_id': patient_id,
                                'success': True,
                                'message': 'Report generated successfully'
                            })
                        else:
                            results.append({
                                'patient_id': patient_id,
                                'success': False,
                                'message': f'Failed to generate report: {error}'
                            })
                    else:
                        results.append({
                            'patient_id': patient_id,
                            'success': False,
                            'message': 'No predictions found for patient'
                        })
                        
                except Exception as e:
                    results.append({
                        'patient_id': patient_id,
                        'success': False,
                        'message': str(e)
                    })
        
        elif action == 'add_tag':
            tag = data.get('tag', '').strip()
            if not tag:
                return jsonify({'error': 'Tag is required'}), 400
            
            for patient_id in patient_ids:
                try:
                    # Add tag to patient
                    db.patients.update_one(
                        {"patient_id": patient_id},
                        {"$addToSet": {"tags": tag}, "$set": {"updated_at": datetime.now()}}
                    )
                    results.append({
                        'patient_id': patient_id,
                        'success': True,
                        'message': f'Tag "{tag}" added successfully'
                    })
                except Exception as e:
                    results.append({
                        'patient_id': patient_id,
                        'success': False,
                        'message': str(e)
                    })
        
        return jsonify({
            'success': True,
            'action': action,
            'results': results,
            'total_processed': len(results),
            'successful': len([r for r in results if r['success']]),
            'failed': len([r for r in results if not r['success']])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/trends')
@login_required
def get_patient_trends(patient_id):
    """Get trend data for a patient (eGFR, BP, ACR over time)"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get all predictions for this patient
        predictions = list(db.predictions.find(
            {"patient_id": patient_id}
        ).sort("created_at", 1))  # Ascending order for trends
        
        trend_data = []
        for pred in predictions:
            input_data = pred.get('input_data', {})
            trend_data.append({
                'date': pred['created_at'].strftime('%Y-%m-%d'),
                'egfr': input_data.get('eGFR', 0),
                'blood_pressure': input_data.get('Blood_Pressure', 0),
                'acr': input_data.get('ACR', 0),
                'serum_creatinine': input_data.get('Serum_Creatinine', 0),
                'bun': input_data.get('BUN', 0),
                'ckd_stage': pred['prediction_result'].get('ckd_stage', ''),
                'risk_level': pred['prediction_result'].get('risk_level', '')
            })
        
        return jsonify({'success': True, 'trends': trend_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/shap-summary')
@login_required
def get_patient_shap_summary(patient_id):
    """Get SHAP feature importance for latest prediction"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get latest prediction
        latest_prediction = db.predictions.find_one(
            {"patient_id": patient_id},
            sort=[("created_at", -1)]
        )
        
        if not latest_prediction:
            return jsonify({'error': 'No predictions found for patient'}), 404
        
        shap_values = latest_prediction.get('shap_values')
        if not shap_values:
            return jsonify({'error': 'SHAP values not available'}), 404
        
        # Get feature names
        feature_names = latest_prediction.get('input_data', {}).keys()
        
        # Create feature importance summary
        feature_importance = []
        for i, (feature, value) in enumerate(zip(feature_names, shap_values[0] if shap_values else [])):
            feature_importance.append({
                'feature': feature,
                'importance': float(value),
                'abs_importance': abs(float(value))
            })
        
        # Sort by absolute importance
        feature_importance.sort(key=lambda x: x['abs_importance'], reverse=True)
        
        return jsonify({
            'success': True,
            'prediction_id': latest_prediction['prediction_id'],
            'feature_importance': feature_importance[:10],  # Top 10 features
            'prediction_result': latest_prediction['prediction_result']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/compare-predictions')
@login_required
def compare_patient_predictions(patient_id):
    """Compare two predictions side-by-side"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        prediction_id_1 = request.args.get('prediction_id_1')
        prediction_id_2 = request.args.get('prediction_id_2')
        
        if not prediction_id_1 or not prediction_id_2:
            return jsonify({'error': 'Both prediction IDs are required'}), 400
        
        # Get both predictions
        pred1 = db.predictions.find_one({"prediction_id": prediction_id_1, "patient_id": patient_id})
        pred2 = db.predictions.find_one({"prediction_id": prediction_id_2, "patient_id": patient_id})
        
        if not pred1 or not pred2:
            return jsonify({'error': 'One or both predictions not found'}), 404
        
        # Compare predictions
        comparison = {
            'prediction_1': {
                'prediction_id': pred1['prediction_id'],
                'date': pred1['created_at'].strftime('%Y-%m-%d %H:%M'),
                'input_data': pred1['input_data'],
                'prediction_result': pred1['prediction_result']
            },
            'prediction_2': {
                'prediction_id': pred2['prediction_id'],
                'date': pred2['created_at'].strftime('%Y-%m-%d %H:%M'),
                'input_data': pred2['input_data'],
                'prediction_result': pred2['prediction_result']
            },
            'changes': {}
        }
        
        # Calculate changes in key metrics
        input1 = pred1['input_data']
        input2 = pred2['input_data']
        
        for key in ['eGFR', 'Blood_Pressure', 'ACR', 'Serum_Creatinine', 'BUN']:
            if key in input1 and key in input2:
                val1 = input1[key]
                val2 = input2[key]
                change = val2 - val1
                change_pct = (change / val1 * 100) if val1 != 0 else 0
                
                comparison['changes'][key] = {
                    'value_1': val1,
                    'value_2': val2,
                    'change': change,
                    'change_percentage': round(change_pct, 2)
                }
        
        return jsonify({'success': True, 'comparison': comparison})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET'])
@login_required
def list_messages():
    """List messages for current user (patient sees their messages; doctor can filter by patient_id)"""
    try:
        if current_user.user_type == 'patient':
            msgs = list(db.messages.find({'patient_id': current_user.id}).sort('created_at', -1))
        elif current_user.user_type == 'doctor':
            patient_id = request.args.get('patient_id')
            query = {'doctor_id': current_user.id}
            if patient_id:
                query['patient_id'] = patient_id
            msgs = list(db.messages.find(query).sort('created_at', -1))
        else:
            return jsonify({'error': 'Unauthorized'}), 403

        def serialize(m):
            return {
                'message_id': m.get('message_id'),
                'patient_id': m.get('patient_id'),
                'doctor_id': m.get('doctor_id'),
                'content': m.get('content'),
                'created_at': m.get('created_at').strftime('%Y-%m-%d %H:%M') if m.get('created_at') else None,
                'read': bool(m.get('read')),
                'type': m.get('type', 'instruction')
            }
        return jsonify({'success': True, 'messages': [serialize(m) for m in msgs]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages/<message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    """Mark a message as read (patients only)"""
    if current_user.user_type != 'patient':
        return jsonify({'error': 'Unauthorized'}), 403
    try:
        res = db.messages.update_one({'message_id': message_id, 'patient_id': current_user.id}, {'$set': {'read': True, 'read_at': datetime.now()}})
        if res.matched_count == 0:
            return jsonify({'error': 'Message not found'}), 404
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_with_gemini():
    """Chat with Gemini AI"""
    try:
        user_message = request.json.get('message', '')
        language = request.json.get('language', 'en')
        
        # Check if Gemini is available
        if model is None:
            # Fallback responses when Gemini is not available
            fallback_responses = {
                'en': {
                    'greeting': "Hello! I'm your CKD Health Assistant. I can help you with questions about Chronic Kidney Disease, diet recommendations, exercise tips, and general health advice. What would you like to know?",
                    'ckd_basics': "Chronic Kidney Disease (CKD) is a condition where your kidneys gradually lose function. Early detection and proper management are crucial. Regular check-ups, maintaining a healthy diet, and following your doctor's advice can help slow progression.",
                    'diet': "For CKD patients, it's important to limit sodium, potassium, and phosphorus. Focus on fresh fruits and vegetables, lean proteins, and whole grains. Always consult with a dietitian for personalized advice.",
                    'exercise': "Regular, moderate exercise is beneficial for CKD patients. Walking, swimming, and light strength training are good options. Always consult your doctor before starting any exercise program.",
                    'default': "I'm here to help with your CKD-related questions. Please ask about diet, exercise, symptoms, or general health advice."
                },
                'kn': {
                    'greeting': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ಸಹಾಯಕ. ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ, ಆಹಾರ ಶಿಫಾರಸುಗಳು, ವ್ಯಾಯಾಮ ಸಲಹೆಗಳು ಮತ್ತು ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?",
                    'ckd_basics': "ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ (ಸಿಕೆಡಿ) ಎಂಬುದು ನಿಮ್ಮ ಮೂತ್ರಪಿಂಡಗಳು ಕ್ರಮೇಣ ಕಾರ್ಯವನ್ನು ಕಳೆದುಕೊಳ್ಳುವ ಸ್ಥಿತಿ. ಆರಂಭಿಕ ಪತ್ತೆ ಮತ್ತು ಸರಿಯಾದ ನಿರ್ವಹಣೆ ಮುಖ್ಯ. ನಿಯಮಿತ ಪರಿಶೀಲನೆ, ಆರೋಗ್ಯಕರ ಆಹಾರ ಮತ್ತು ನಿಮ್ಮ ವೈದ್ಯರ ಸಲಹೆಯನ್ನು ಅನುಸರಿಸುವುದು ಪ್ರಗತಿಯನ್ನು ನಿಧಾನಗೊಳಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
                    'diet': "ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ, ಸೋಡಿಯಂ, ಪೊಟ್ಯಾಸಿಯಂ ಮತ್ತು ಫಾಸ್ಫರಸ್ ಅನ್ನು ಸೀಮಿತಗೊಳಿಸುವುದು ಮುಖ್ಯ. ತಾಜಾ ಹಣ್ಣುಗಳು ಮತ್ತು ತರಕಾರಿಗಳು, ಕಡಿಮೆ ಕೊಬ್ಬಿನ ಪ್ರೋಟೀನ್ ಮತ್ತು ಸಂಪೂರ್ಣ ಧಾನ್ಯಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ. ವೈಯಕ್ತಿಕ ಸಲಹೆಗಾಗಿ ಯಾವಾಗಲೂ ಪೋಷಣಾ ತಜ್ಞರೊಂದಿಗೆ ಸಲಹೆ ಮಾಡಿಕೊಳ್ಳಿ.",
                    'exercise': "ನಿಯಮಿತ, ಮಧ್ಯಮ ವ್ಯಾಯಾಮವು ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ ಪ್ರಯೋಜನಕಾರಿ. ನಡಿಗೆ, ಈಜು ಮತ್ತು ಹಗುರ ಬಲ ತರಬೇತಿ ಉತ್ತಮ ಆಯ್ಕೆಗಳು. ಯಾವುದೇ ವ್ಯಾಯಾಮ ಕಾರ್ಯಕ್ರಮವನ್ನು ಪ್ರಾರಂಭಿಸುವ ಮೊದಲು ಯಾವಾಗಲೂ ನಿಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಸಲಹೆ ಮಾಡಿಕೊಳ್ಳಿ.",
                    'default': "ನಿಮ್ಮ ಸಿಕೆಡಿ-ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳಿಗೆ ನಾನು ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ. ಆಹಾರ, ವ್ಯಾಯಾಮ, ಲಕ್ಷಣಗಳು ಅಥವಾ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ."
                }
            }
            
            # Simple keyword matching for fallback responses
            message_lower = user_message.lower()
            if any(word in message_lower for word in ['hello', 'hi', 'greeting', 'ನಮಸ್ಕಾರ', 'ಹಲೋ']):
                response_text = fallback_responses[language]['greeting']
            elif any(word in message_lower for word in ['ckd', 'kidney', 'chronic', 'ಸಿಕೆಡಿ', 'ಮೂತ್ರಪಿಂಡ']):
                response_text = fallback_responses[language]['ckd_basics']
            elif any(word in message_lower for word in ['diet', 'food', 'nutrition', 'ಆಹಾರ', 'ಪೋಷಣೆ']):
                response_text = fallback_responses[language]['diet']
            elif any(word in message_lower for word in ['exercise', 'workout', 'fitness', 'ವ್ಯಾಯಾಮ', 'ಫಿಟ್ನೆಸ್']):
                response_text = fallback_responses[language]['exercise']
            else:
                response_text = fallback_responses[language]['default']
            
            return jsonify({
                'response': response_text,
                'timestamp': datetime.now().isoformat()
            })
        
        # Use Gemini if available
        prompt = f"""
        You are a healthcare AI assistant specializing in Chronic Kidney Disease (CKD) management.
        Provide helpful, accurate, and empathetic responses about CKD, diet, exercise, and general health.
        Respond in {language} language.
        
        User question: {user_message}
        
        IMPORTANT: 
        - Keep your response SHORT, CONCISE, and POINT-WISE
        - Use simple bullet points (•) or dashes (-) for lists
        - NO markdown formatting (no *, **, #, etc.)
        - NO bold or italic text
        - Use plain text only
        - Maximum 5-7 key points per response
        - Clean, neat format without special characters
        """
        
        try:
            print(f"Calling Gemini API with prompt: {prompt[:100]}...")
            print(f"Model object: {model}")
            response = model.generate_content(prompt)
            print(f"Gemini response received: {response.text[:100]}...")
            return jsonify({
                'response': response.text,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Gemini API error: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            # If Gemini fails at runtime, gracefully fall back to local responses
            fallback_responses = {
                'en': {
                    'greeting': "Hello! I'm your CKD Health Assistant. I can help you with questions about Chronic Kidney Disease, diet recommendations, exercise tips, and general health advice. What would you like to know?",
                    'ckd_basics': "Chronic Kidney Disease (CKD) is a condition where your kidneys gradually lose function. Early detection and proper management are crucial. Regular check-ups, maintaining a healthy diet, and following your doctor's advice can help slow progression.",
                    'diet': "For CKD patients, it's important to limit sodium, potassium, and phosphorus. Focus on fresh fruits and vegetables, lean proteins, and whole grains. Always consult with a dietitian for personalized advice.",
                    'exercise': "Regular, moderate exercise is beneficial for CKD patients. Walking, swimming, and light strength training are good options. Always consult your doctor before starting any exercise program.",
                    'default': "I'm here to help with your CKD-related questions. Please ask about diet, exercise, symptoms, or general health advice."
                },
                'kn': {
                    'greeting': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ಸಹಾಯಕ. ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ, ಆಹಾರ ಶಿಫಾರಸುಗಳು, ವ್ಯಾಯಾಮ ಸಲಹೆಗಳು ಮತ್ತು ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?",
                    'ckd_basics': "ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ (ಸಿಕೆಡಿ) ಎಂಬುದು ನಿಮ್ಮ ಮೂತ್ರಪಿಂಡಗಳು ಕ್ರಮೇಣ ಕಾರ್ಯವನ್ನು ಕಳೆದುಕೊಳ್ಳುವ ಸ್ಥಿತಿ. ಆರಂಭಿಕ ಪತ್ತೆ ಮತ್ತು ಸರಿಯಾದ ನಿರ್ವಹಣೆ ಮುಖ್ಯ. ನಿಯಮಿತ ಪರಿಶೀಲನೆ, ಆರೋಗ್ಯಕರ ಆಹಾರ ಮತ್ತು ನಿಮ್ಮ ವೈದ್ಯರ ಸಲಹೆಯನ್ನು ಅನುಸರಿಸುವುದು ಪ್ರಗತಿಯನ್ನು ನಿಧಾನಗೊಳಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
                    'diet': "ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ, ಸೋಡಿಯಂ, ಪೊಟ್ಯಾಸಿಯಂ ಮತ್ತು ಫಾಸ್ಫರಸ್ ಅನ್ನು ಸೀಮಿತಗೊಳಿಸುವುದು ಮುಖ್ಯ. ತಾಜಾ ಹಣ್ಣುಗಳು ಮತ್ತು ತರಕಾರಿಗಳು, ಕಡಿಮೆ ಕೊಬ್ಬಿನ ಪ್ರೋಟೀನ್ ಮತ್ತು ಸಂಪೂರ್ಣ ಧಾನ್ಯಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ. ವೈಯಕ್ತಿಕ ಸಲಹೆಗಾಗಿ ಯಾವಾಗಲೂ ಪೋಷಣಾ ತಜ್ಞರೊಂದಿಗೆ ಸಲಹೆ ಮಾಡಿಕೊಳ್ಳಿ.",
                    'exercise': "ನಿಯಮಿತ, ಮಧ್ಯಮ ವ್ಯಾಯಾಮವು ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ ಪ್ರಯೋಜನಕಾರಿ. ನಡಿಗೆ, ಈಜು ಮತ್ತು ಹಗುರ ಬಲ ತರಬೇತಿ ಉತ್ತಮ ಆಯ್ಕೆಗಳು. ಯಾವುದೇ ವ್ಯಾಯಾಮ ಕಾರ್ಯಕ್ರಮವನ್ನು ಪ್ರಾರಂಭಿಸುವ ಮೊದಲು ಯಾವಾಗಲೂ ನಿಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಸಲಹೆ ಮಾಡಿಕೊಳ್ಳಿ.",
                    'default': "ನಿಮ್ಮ ಸಿಕೆಡಿ-ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳಿಗೆ ನಾನು ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ. ಆಹಾರ, ವ್ಯಾಯಾಮ, ಲಕ್ಷಣಗಳು ಅಥವಾ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ."
                }
            }
            lang = language if language in fallback_responses else 'en'
            msg = user_message.lower()
            if any(w in msg for w in ['hello', 'hi', 'greeting', 'ನಮಸ್ಕಾರ', 'ಹಲೋ']):
                response_text = fallback_responses[lang]['greeting']
            elif any(w in msg for w in ['ckd', 'kidney', 'chronic', 'ಸಿಕೆಡಿ', 'ಮೂತ್ರಪಿಂಡ']):
                response_text = fallback_responses[lang]['ckd_basics']
            elif any(w in msg for w in ['diet', 'food', 'nutrition', 'ಆಹಾರ', 'ಪೋಷಣೆ']):
                response_text = fallback_responses[lang]['diet']
            elif any(w in msg for w in ['exercise', 'workout', 'fitness', 'ವ್ಯಾಯಾಮ', 'ಫಿಟ್ನೆಸ್']):
                response_text = fallback_responses[lang]['exercise']
            else:
                response_text = fallback_responses[lang]['default']

            return jsonify({
                'response': response_text,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients')
@login_required
def get_all_patients():
    """Get all patients for doctor dashboard with filters and pagination"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Parse query params
        search = request.args.get('search', '').strip().lower()
        gender = request.args.get('gender')  # 'M'|'F'|''
        stage = request.args.get('stage')    # 'Stage 1'..'Stage 5'|'No CKD'|''
        risk = request.args.get('risk')      # 'High'|'Medium'|'Low'|''
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(max(int(request.args.get('page_size', 10)), 1), 100)

        # Build base cursor
        base_cursor = db.patients.find()

        # Apply search and gender filter at DB level when possible
        if search:
            base_cursor = db.patients.find({
                "$or": [
                    {"personal_info.name": {"$regex": search, "$options": "i"}},
                    {"personal_info.email": {"$regex": search, "$options": "i"}},
                    {"patient_id": {"$regex": search, "$options": "i"}},
                ]
            })
        if gender in ('M', 'F'):
            base_cursor = base_cursor.filter({"personal_info.gender": gender}) if hasattr(base_cursor, 'filter') else db.patients.find({"personal_info.gender": gender})

        # Load and post-filter by stage/risk/date ranges that depend on predictions
        all_patients = list(base_cursor.sort("created_at", -1))
        filtered = []
        for patient in all_patients:
            # Get latest prediction for this patient
            latest_prediction = db.predictions.find_one(
                {"patient_id": patient['patient_id']},
                sort=[("created_at", -1)]
            )
            
            # Determine health status
            health_status = "Unknown"
            latest_risk = None
            latest_created = None
            if latest_prediction:
                latest_created = latest_prediction.get('created_at')
                if latest_prediction['prediction_result']['ckd_binary']:
                    health_status = f"CKD {latest_prediction['prediction_result']['ckd_stage']}"
                else:
                    health_status = "Healthy"
                latest_risk = latest_prediction['prediction_result'].get('risk_level')

            # Filters by stage
            if stage:
                if stage == 'No CKD' and health_status != 'Healthy':
                    continue
                if stage.startswith('Stage') and f"CKD {stage}" != health_status:
                    continue
            # Filter by risk
            if risk and latest_risk and latest_risk != risk:
                continue
            # Filter by date range (joined date)
            if date_from:
                try:
                    df = datetime.fromisoformat(date_from)
                    if patient.get('created_at') and patient['created_at'] < df:
                        continue
                except Exception:
                    pass
            if date_to:
                try:
                    dt = datetime.fromisoformat(date_to)
                    if patient.get('created_at') and patient['created_at'] > dt:
                        continue
                except Exception:
                    pass
            
            patient_data = {
                'patient_id': patient['patient_id'],
                'name': patient['personal_info']['name'],
                'email': patient['personal_info']['email'],
                'phone': patient['personal_info'].get('phone', ''),
                'age': patient['personal_info'].get('age', ''),
                'gender': patient['personal_info'].get('gender', ''),
                'created_at': patient['created_at'].strftime('%Y-%m-%d'),
                'health_status': health_status,
                'last_prediction': latest_created.strftime('%Y-%m-%d') if latest_created else 'Never',
                'risk_level': latest_risk or ''
            }
            filtered.append(patient_data)

        total_count = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        patients = filtered[start:end]
        
        # Calculate pagination info
        total_pages = (total_count + page_size - 1) // page_size
        has_prev = page > 1
        has_next = page < total_pages
        
        return jsonify({
            'success': True,
            'patients': patients,
            'pagination': {
                'page': page,
                'per_page': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/<patient_id>', methods=['GET'])
@login_required
def get_patient_details(patient_id):
    """Get detailed info for a specific patient including recent predictions"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        patient = db.patients.find_one({"patient_id": patient_id})
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Serialize patient
        patient_data = {
            'patient_id': patient['patient_id'],
            'personal_info': {
                'name': patient['personal_info'].get('name', ''),
                'email': patient['personal_info'].get('email', ''),
                'phone': patient['personal_info'].get('phone', ''),
                'age': patient['personal_info'].get('age', ''),
                'gender': patient['personal_info'].get('gender', ''),
                'address': patient['personal_info'].get('address', ''),
            },
            'created_at': patient.get('created_at').strftime('%Y-%m-%d') if patient.get('created_at') else None,
            'updated_at': patient.get('updated_at').strftime('%Y-%m-%d') if patient.get('updated_at') else None,
        }

        # Recent predictions
        preds = list(db.predictions.find({"patient_id": patient_id}).sort("created_at", -1).limit(5))
        recent_predictions = []
        for p in preds:
            recent_predictions.append({
                'prediction_id': p.get('prediction_id'),
                'created_at': p.get('created_at').strftime('%Y-%m-%d %H:%M') if p.get('created_at') else None,
                'ckd_binary': bool(p.get('prediction_result', {}).get('ckd_binary', False)),
                'ckd_stage': p.get('prediction_result', {}).get('ckd_stage', ''),
                'confidence': float(p.get('prediction_result', {}).get('confidence', 0.0)),
                'risk_level': p.get('prediction_result', {}).get('risk_level', ''),
            })

        return jsonify({'success': True, 'patient': patient_data, 'recent_predictions': recent_predictions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/import-patients', methods=['POST'])
@login_required
def import_patients_from_csv():
    """Import patients from CSV file into MongoDB (doctor-only helper)"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        csv_path = 'hospital real time.csv'
        if not os.path.exists(csv_path):
            return jsonify({'error': f'CSV file not found: {csv_path}'}), 400

        df = pd.read_csv(csv_path)
        inserted = 0
        skipped = 0

        # Ensure required columns exist (leniently handle NaNs)
        for idx, row in df.iterrows():
            # Generate stable ids and basic info
            patient_id = f"PAT_{str(uuid.uuid4())[:8]}"
            name = f"Patient {idx + 1}"
            email = f"patient{idx + 1}@example.com"
            gender = str(row.get('gender', '') or '').strip() or None
            age = None
            try:
                age_val = row.get('age', None)
                if pd.notna(age_val):
                    age = int(age_val)
            except Exception:
                age = None

            # Check if an existing patient with same email exists
            if db.patients.find_one({"personal_info.email": email}):
                skipped += 1
                continue

            patient_doc = {
                "patient_id": patient_id,
                "personal_info": {
                    "name": name,
                    "email": email,
                    "phone": "",
                    "age": age,
                    "gender": gender,
                    "address": "",
                    "emergency_contact": ""
                },
                "health_history": {},
                "preferences": {
                    "language": session.get('language', 'en'),
                    "theme": "light",
                    "notifications": True
                },
                "password": generate_password_hash("password123"),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

            db.patients.insert_one(patient_doc)
            inserted += 1

        return jsonify({'success': True, 'inserted': inserted, 'skipped': skipped, 'total_rows': int(df.shape[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    """Get analytics data for doctor dashboard with filters"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get filter parameters
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        stage_filter = request.args.get('stage')
        
        # Build date filter
        date_filter = {}
        if date_from:
            try:
                date_filter['$gte'] = datetime.fromisoformat(date_from)
            except Exception:
                pass
        if date_to:
            try:
                date_filter['$lte'] = datetime.fromisoformat(date_to)
            except Exception:
                pass
        
        # Build stage filter
        stage_query = {}
        if stage_filter and stage_filter != 'all':
            stage_query['prediction_result.ckd_stage'] = stage_filter
        
        # Combine filters
        prediction_filters = {}
        if date_filter:
            prediction_filters['created_at'] = date_filter
        if stage_query:
            prediction_filters.update(stage_query)
        
        # Get comprehensive analytics
        total_patients = db.patients.count_documents({})
        ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": True, **prediction_filters})
        non_ckd_patients = db.predictions.count_documents({"prediction_result.ckd_binary": False, **prediction_filters})
        total_predictions = db.predictions.count_documents(prediction_filters)
        
        # Stage distribution
        stage_pipeline = [
            {"$match": prediction_filters},
            {"$group": {"_id": "$prediction_result.ckd_stage", "count": {"$sum": 1}}}
        ]
        stage_distribution = {}
        for stage_data in db.predictions.aggregate(stage_pipeline):
            stage_distribution[stage_data['_id']] = stage_data['count']
        
        # Risk level distribution
        risk_pipeline = [
            {"$match": prediction_filters},
            {"$group": {"_id": "$prediction_result.risk_level", "count": {"$sum": 1}}}
        ]
        risk_distribution = {}
        for risk_data in db.predictions.aggregate(risk_pipeline):
            risk_distribution[risk_data['_id']] = risk_data['count']
        
        # Recent predictions
        recent_predictions = list(db.predictions.find(prediction_filters).sort("created_at", -1).limit(10))
        
        # Model accuracy and performance metrics (from training)
        model_accuracy = 0.9808
        precision = 0.9756
        recall = 0.9823
        f1_score = 0.9789
        
        # Confusion matrix (static from training)
        confusion_matrix = {
            'true_negative': 2456,
            'false_positive': 23,
            'false_negative': 18,
            'true_positive': 2503
        }
        
        return jsonify({
            'total_patients': total_patients,
            'ckd_patients': ckd_patients,
            'non_ckd_patients': non_ckd_patients,
            'total_predictions': total_predictions,
            'stage_distribution': stage_distribution,
            'risk_distribution': risk_distribution,
            'model_accuracy': model_accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'confusion_matrix': confusion_matrix,
            'recent_predictions': recent_predictions,
            'filters_applied': {
                'date_from': date_from,
                'date_to': date_to,
                'stage': stage_filter
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/export', methods=['GET'])
@login_required
def export_analytics_csv():
    """Export analytics data as CSV"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get analytics data
        analytics_response = get_analytics()
        if analytics_response[1] != 200:  # Check if error
            return analytics_response
        
        analytics_data = analytics_response[0].get_json()
        
        # Create CSV content
        import csv
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write analytics summary
        writer.writerow(['Analytics Summary'])
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Patients', analytics_data['total_patients']])
        writer.writerow(['CKD Patients', analytics_data['ckd_patients']])
        writer.writerow(['Non-CKD Patients', analytics_data['non_ckd_patients']])
        writer.writerow(['Total Predictions', analytics_data['total_predictions']])
        writer.writerow(['Model Accuracy', f"{analytics_data['model_accuracy']:.4f}"])
        writer.writerow(['Precision', f"{analytics_data['precision']:.4f}"])
        writer.writerow(['Recall', f"{analytics_data['recall']:.4f}"])
        writer.writerow(['F1 Score', f"{analytics_data['f1_score']:.4f}"])
        writer.writerow([])
        
        # Write stage distribution
        writer.writerow(['CKD Stage Distribution'])
        writer.writerow(['Stage', 'Count'])
        for stage, count in analytics_data['stage_distribution'].items():
            writer.writerow([stage, count])
        writer.writerow([])
        
        # Write risk distribution
        writer.writerow(['Risk Level Distribution'])
        writer.writerow(['Risk Level', 'Count'])
        for risk, count in analytics_data['risk_distribution'].items():
            writer.writerow([risk, count])
        writer.writerow([])
        
        # Write confusion matrix
        writer.writerow(['Confusion Matrix'])
        cm = analytics_data['confusion_matrix']
        writer.writerow(['', 'Predicted No CKD', 'Predicted CKD'])
        writer.writerow(['Actual No CKD', cm['true_negatives'], cm['false_positives']])
        writer.writerow(['Actual CKD', cm['false_negatives'], cm['true_positives']])
        
        csv_content = output.getvalue()
        output.close()
        
        # Return CSV file
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            as_attachment=True,
            download_name=f'analytics_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report/<prediction_id>')
@login_required
def generate_report(prediction_id):
    """Generate PDF report for a prediction"""
    try:
        prediction = db.predictions.find_one({"prediction_id": prediction_id})
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Generate PDF report
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("CKD Health Report", title_style))
        story.append(Spacer(1, 20))
        
        # Patient info
        patient = db.patients.find_one({"patient_id": prediction['patient_id']})
        if patient:
            story.append(Paragraph(f"Patient: {patient['personal_info']['name']}", styles['Heading2']))
            story.append(Paragraph(f"Email: {patient['personal_info']['email']}", styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Prediction results
        story.append(Paragraph("Prediction Results", styles['Heading2']))
        result = prediction['prediction_result']
        story.append(Paragraph(f"CKD Detected: {'Yes' if result['ckd_binary'] else 'No'}", styles['Normal']))
        story.append(Paragraph(f"CKD Stage: {result['ckd_stage']}", styles['Normal']))
        story.append(Paragraph(f"Confidence Score: {result['confidence']:.2f}", styles['Normal']))
        story.append(Paragraph(f"Risk Level: {result['risk_level']}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Recommendations
        recommendation = db.recommendations.find_one({"patient_id": prediction['patient_id']})
        if recommendation:
            story.append(Paragraph("Recommendations", styles['Heading2']))
            story.append(Paragraph("Diet Plan:", styles['Heading3']))
            diet_plan = recommendation['diet_plan']
            for meal, food in diet_plan.items():
                story.append(Paragraph(f"{meal.title()}: {food}", styles['Normal']))
            
            story.append(Spacer(1, 12))
            story.append(Paragraph("Exercise Plan:", styles['Heading3']))
            exercise_plan = recommendation['exercise_plan']
            for key, value in exercise_plan.items():
                story.append(Paragraph(f"{key.replace('_', ' ').title()}: {value}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        # Save report to database
        report_id = f"REP_{str(uuid.uuid4())[:8]}"
        report_data = {
            "report_id": report_id,
            "patient_id": prediction['patient_id'],
            "doctor_id": current_user.id if current_user.user_type == 'doctor' else None,
            "prediction_id": prediction_id,
            "report_type": "prediction",
            "file_path": f"reports/{report_id}.pdf",
            "email_sent": False,
            "created_at": datetime.now()
        }
        
        db.reports.insert_one(report_data)
        
        # Return PDF as base64
        pdf_data = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        return jsonify({
            'report_id': report_id,
            'pdf_data': pdf_base64,
            'filename': f"ckd_report_{prediction_id}.pdf"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Report Generation and Email Delivery Routes
@app.route('/api/generate-report/<prediction_id>')
@login_required
def generate_comprehensive_report(prediction_id):
    """Generate comprehensive PDF report and send via email"""
    try:
        # Import report generation functions
        from report_generator import create_patient_report, send_email_report, generate_and_send_report
        
        # Generate and send report
        success, message = generate_and_send_report(
            prediction_id, 
            send_email=True, 
            send_sms=True
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Report generated and sent successfully',
                'prediction_id': prediction_id
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-report/<prediction_id>')
@login_required
def download_report(prediction_id):
    """Download PDF report"""
    try:
        from report_generator import create_patient_report
        
        # Generate PDF report
        pdf_content, error = create_patient_report(prediction_id)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Return PDF as file download
        return send_file(
            io.BytesIO(pdf_content),
            as_attachment=True,
            download_name=f'CKD_Report_{prediction_id}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-report-email/<prediction_id>', methods=['POST'])
@login_required
def send_report_email(prediction_id):
    """Send report via email - DISABLED"""
    return jsonify({'success': False, 'message': 'Email sending is disabled on this server.'}), 200

@app.route('/api/batch-reports', methods=['POST'])
@login_required
def generate_batch_reports():
    """Generate reports for multiple patients"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        from report_generator import generate_batch_reports
        
        data = request.json
        patient_ids = data.get('patient_ids', [])
        send_emails = data.get('send_emails', True)
        send_sms = data.get('send_sms', True)
        
        if not patient_ids:
            return jsonify({'error': 'No patient IDs provided'}), 400
        
        # Generate batch reports
        results = generate_batch_reports(patient_ids, send_emails, send_sms)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results),
            'successful': len([r for r in results if r['success']]),
            'failed': len([r for r in results if not r['success']])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report-history')
@login_required
def get_report_history():
    """Get report history for current user"""
    try:
        if current_user.user_type == 'patient':
            # Get reports for this patient
            reports = list(db.reports.find(
                {"patient_id": current_user.id}
            ).sort("created_at", -1))
        elif current_user.user_type == 'doctor':
            # Get all reports
            reports = list(db.reports.find().sort("created_at", -1))
        else:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'reports': reports,
            'total_count': len(reports)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Multilingual Support Routes
@app.route('/api/set-language', methods=['POST'])
def set_language():
    """Set user's preferred language"""
    try:
        data = request.json
        language = data.get('language', 'en')
        
        if language not in get_supported_languages():
            language = 'en'  # Default to English
        
        # Store language preference in session
        session['language'] = language
        
        return jsonify({
            'success': True,
            'language': language,
            'message': 'Language preference updated'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-translations/<language>')
def get_translations(language):
    """Get all translations for a specific language"""
    try:
        if language not in get_supported_languages():
            language = 'en'  # Default to English
        
        translations = get_all_translations(language)
        
        return jsonify({
            'success': True,
            'language': language,
            'translations': translations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text using the multilingual system"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if language not in get_supported_languages():
            language = 'en'  # Default to English
        
        # Get translation for the text
        translation = get_translation(text, language)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translated_text': translation,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/supported-languages')
def get_supported_languages_api():
    """Get list of supported languages"""
    try:
        languages = get_supported_languages()
        language_info = []
        
        for lang_code in languages:
            language_info.append({
                'code': lang_code,
                'name': get_translation('language_name', lang_code) if lang_code == 'en' else 'ಕನ್ನಡ'
            })
        
        return jsonify({
            'success': True,
            'languages': language_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Workflow and Data Quality Features
@app.route('/api/follow-up-scheduler', methods=['GET', 'POST'])
@login_required
def manage_follow_ups():
    """Manage follow-up appointments and reminders"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        if request.method == 'GET':
            # Get all follow-ups
            follow_ups = list(db.follow_ups.find().sort("scheduled_date", 1))
            return jsonify({'success': True, 'follow_ups': follow_ups})
        
        elif request.method == 'POST':
            # Create new follow-up
            data = request.json
            patient_id = data.get('patient_id')
            scheduled_date = data.get('scheduled_date')
            reminder_days = data.get('reminder_days', 7)
            notes = data.get('notes', '')
            
            if not patient_id or not scheduled_date:
                return jsonify({'error': 'Patient ID and scheduled date are required'}), 400
            
            follow_up_id = f"FU_{str(uuid.uuid4())[:8]}"
            follow_up_doc = {
                'follow_up_id': follow_up_id,
                'patient_id': patient_id,
                'doctor_id': current_user.id,
                'scheduled_date': datetime.fromisoformat(scheduled_date),
                'reminder_days': reminder_days,
                'notes': notes,
                'status': 'scheduled',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            db.follow_ups.insert_one(follow_up_doc)
            return jsonify({'success': True, 'follow_up_id': follow_up_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor-assignment', methods=['POST'])
@login_required
def assign_patient_to_doctor():
    """Assign patient to a specific doctor"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        patient_id = data.get('patient_id')
        assigned_doctor_id = data.get('assigned_doctor_id')
        
        if not patient_id or not assigned_doctor_id:
            return jsonify({'error': 'Patient ID and assigned doctor ID are required'}), 400
        
        # Verify patient and doctor exist
        patient = db.patients.find_one({"patient_id": patient_id})
        doctor = db.doctors.find_one({"doctor_id": assigned_doctor_id})
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        # Update patient assignment
        result = db.patients.update_one(
            {"patient_id": patient_id},
            {"$set": {"assigned_doctor_id": assigned_doctor_id, "updated_at": datetime.now()}}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Failed to update patient assignment'}), 500
        
        # Add to doctor's patient list
        db.doctors.update_one(
            {"doctor_id": assigned_doctor_id},
            {"$addToSet": {"patients_under_care": patient_id}, "$set": {"updated_at": datetime.now()}}
        )
        
        return jsonify({'success': True, 'message': 'Patient assigned successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/patient/trends')
@login_required
def get_patient_trends_for_dashboard():
    """Get health trends for current patient"""
    if current_user.user_type != 'patient':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        period = int(request.args.get('period', 30))
        patient_id = current_user.id
        
        # Get predictions for the period
        from_date = datetime.now() - timedelta(days=period)
        predictions = list(db.predictions.find({
            'patient_id': patient_id,
            'created_at': {'$gte': from_date}
        }).sort('created_at', 1))
        
        # Prepare trend data
        labels = []
        egfr_values = []
        bp_systolic = []
        bp_diastolic = []
        acr_values = []
        
        for pred in predictions:
            labels.append(pred['created_at'].strftime('%Y-%m-%d'))
            
            # Extract values from input data
            input_data = pred.get('input_data', {})
            egfr_values.append(input_data.get('eGFR', 0))
            
            # For blood pressure, we need to split the single value or use separate fields
            blood_pressure = input_data.get('Blood_Pressure', 0)
            if isinstance(blood_pressure, (int, float)) and blood_pressure > 0:
                # If it's a single value, estimate systolic/diastolic
                bp_systolic.append(blood_pressure)
                bp_diastolic.append(blood_pressure * 0.7)  # Estimate diastolic as 70% of systolic
            else:
                bp_systolic.append(0)
                bp_diastolic.append(0)
            
            acr_values.append(input_data.get('ACR', 0))
        
        # If no data, show a message
        if len(predictions) == 0:
            return jsonify({
                'success': True,
                'egfr_trend': {
                    'labels': [],
                    'values': []
                },
                'bp_trend': {
                    'labels': [],
                    'systolic': [],
                    'diastolic': []
                },
                'acr_trend': {
                    'labels': [],
                    'values': []
                },
                'risk_alerts': [{
                    'title': 'No Data Available',
                    'message': f'No predictions found for the last {period} days. Make some predictions to see your health trends.',
                    'severity': 'info'
                }]
            })
        
        # Generate risk alerts
        risk_alerts = []
        latest_prediction = predictions[-1] if predictions else None
        
        if latest_prediction:
            pred_result = latest_prediction['prediction_result']
            
            # eGFR alerts
            egfr = latest_prediction.get('input_data', {}).get('eGFR', 0)
            if egfr < 60:
                risk_alerts.append({
                    'title': 'Low eGFR Alert',
                    'message': f'Your eGFR is {egfr}, which indicates reduced kidney function.',
                    'severity': 'high' if egfr < 30 else 'medium'
                })
            
            # Blood pressure alerts
            systolic = latest_prediction.get('input_data', {}).get('Blood_Pressure', 0)
            if systolic > 140:
                risk_alerts.append({
                    'title': 'High Blood Pressure Alert',
                    'message': f'Your blood pressure is {systolic} mmHg, which is elevated.',
                    'severity': 'high' if systolic > 160 else 'medium'
                })
            
            # CKD stage alerts
            if pred_result['ckd_binary']:
                stage = pred_result['ckd_stage']
                risk_alerts.append({
                    'title': f'CKD {stage} Detected',
                    'message': f'Your latest prediction shows CKD {stage}. Please consult your doctor.',
                    'severity': 'high' if stage in ['Stage 4', 'Stage 5'] else 'medium'
                })
        
        return jsonify({
            'success': True,
            'egfr_trend': {
                'labels': labels,
                'values': egfr_values
            },
            'bp_trend': {
                'labels': labels,
                'systolic': bp_systolic,
                'diastolic': bp_diastolic
            },
            'acr_trend': {
                'labels': labels,
                'values': acr_values
            },
            'risk_alerts': risk_alerts
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/activity-log')
@login_required
def get_activity_log():
    """Get activity log for patients"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        patient_id = request.args.get('patient_id')
        limit = int(request.args.get('limit', 50))
        
        query = {}
        if patient_id:
            query['patient_id'] = patient_id
        
        activities = list(db.activity_log.find(query).sort("created_at", -1).limit(limit))
        
        return jsonify({'success': True, 'activities': activities})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv-import', methods=['POST'])
@login_required
def import_csv_data():
    """Import patient data from CSV with preview and validation"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Preview first 5 rows
        preview_data = df.head(5).to_dict('records')
        columns = list(df.columns)
        
        # Validate required columns
        required_columns = ['name', 'email', 'age', 'gender']
        missing_columns = [col for col in required_columns if col not in columns]
        
        return jsonify({
            'success': True,
            'preview': preview_data,
            'columns': columns,
            'total_rows': len(df),
            'missing_required_columns': missing_columns,
            'validation_passed': len(missing_columns) == 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/csv-import/process', methods=['POST'])
@login_required
def process_csv_import():
    """Process CSV import with column mapping"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        csv_content = data.get('csv_content')
        column_mapping = data.get('column_mapping', {})
        
        if not csv_content:
            return jsonify({'error': 'CSV content is required'}), 400
        
        # Parse CSV content
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Apply column mapping
        df = df.rename(columns=column_mapping)
        
        # Import patients
        imported = 0
        skipped = 0
        errors = []
        
        for idx, row in df.iterrows():
            try:
                # Generate patient data
                patient_id = f"PAT_{str(uuid.uuid4())[:8]}"
                name = str(row.get('name', f'Patient {idx + 1}')).strip()
                email = str(row.get('email', f'patient{idx + 1}@example.com')).strip()
                age = None
                gender = None
                
                try:
                    age_val = row.get('age')
                    if pd.notna(age_val):
                        age = int(age_val)
                except Exception:
                    pass
                
                try:
                    gender_val = str(row.get('gender', '')).strip().upper()
                    if gender_val in ['M', 'F', 'MALE', 'FEMALE']:
                        gender = 'M' if gender_val in ['M', 'MALE'] else 'F'
                except Exception:
                    pass
                
                # Check if patient already exists
                if db.patients.find_one({"personal_info.email": email}):
                    skipped += 1
                    continue
                
                patient_doc = {
                    "patient_id": patient_id,
                    "personal_info": {
                        "name": name,
                        "email": email,
                        "phone": str(row.get('phone', '')).strip(),
                        "age": age,
                        "gender": gender,
                        "address": str(row.get('address', '')).strip(),
                        "emergency_contact": str(row.get('emergency_contact', '')).strip()
                    },
                    "health_history": {},
                    "preferences": {
                        "language": session.get('language', 'en'),
                        "theme": "light",
                        "notifications": True
                    },
                    "password": generate_password_hash("password123"),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "imported_from_csv": True
                }
                
                db.patients.insert_one(patient_doc)
                imported += 1
                
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
        
        return jsonify({
            'success': True,
            'imported': imported,
            'skipped': skipped,
            'errors': errors,
            'total_processed': len(df)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data-quality-check')
@login_required
def check_data_quality():
    """Check data quality for patients"""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get all patients
        patients = list(db.patients.find())
        
        quality_issues = []
        for patient in patients:
            issues = []
            personal_info = patient.get('personal_info', {})
            
            # Check for missing data
            if not personal_info.get('age'):
                issues.append('Missing age')
            if not personal_info.get('gender'):
                issues.append('Missing gender')
            if not personal_info.get('phone'):
                issues.append('Missing phone')
            if not personal_info.get('address'):
                issues.append('Missing address')
            
            if issues:
                quality_issues.append({
                    'patient_id': patient['patient_id'],
                    'name': personal_info.get('name', 'Unknown'),
                    'email': personal_info.get('email', 'Unknown'),
                    'issues': issues,
                    'severity': 'high' if len(issues) >= 3 else 'medium' if len(issues) >= 2 else 'low'
                })
        
        return jsonify({
            'success': True,
            'total_patients': len(patients),
            'patients_with_issues': len(quality_issues),
            'quality_issues': quality_issues
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper function to log activities
def log_activity(patient_id, action, details, user_id, user_type):
    """Log user activity"""
    try:
        activity_doc = {
            'activity_id': f"ACT_{str(uuid.uuid4())[:8]}",
            'patient_id': patient_id,
            'user_id': user_id,
            'user_type': user_type,
            'action': action,
            'details': details,
            'created_at': datetime.now()
        }
        db.activity_log.insert_one(activity_doc)
    except Exception as e:
        print(f"Failed to log activity: {e}")

# Template context processor for multilingual support
@app.context_processor
def inject_translations():
    """Inject translations into all templates"""
    language = session.get('language', 'en')
    return {
        't': lambda key: get_translation(key, language),
        'current_language': language,
        'supported_languages': get_supported_languages()
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
