# Multilingual Support System (English + Kannada)

"""
This module provides multilingual support for the Smart CKD Health Management System
with English and Kannada language support.
"""

# Language translations
TRANSLATIONS = {
    'en': {
        # App Info
        'app_name': 'Smart CKD Health',
        'app_description': 'AI-powered Chronic Kidney Disease detection and management system.',
        'copyright': '© 2025 Smart CKD Health. All rights reserved.',
        
        # Navigation
        'home': 'Home',
        'dashboard': 'Dashboard',
        'login': 'Login',
        'signup': 'Sign Up',
        'logout': 'Logout',
        'profile': 'Profile',
        'settings': 'Settings',
        
        # Authentication
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'name': 'Name',
        'phone': 'Phone',
        'user_type': 'User Type',
        'patient': 'Patient',
        'doctor': 'Doctor',
        'sign_in': 'Sign In',
        'create_account': 'Create Account',
        'forgot_password': 'Forgot Password?',
        
        # Health Parameters
        'age': 'Age',
        'gender': 'Gender',
        'blood_pressure': 'Blood Pressure',
        'sugar_level': 'Sugar Level',
        'albumin': 'Albumin',
        'serum_creatinine': 'Serum Creatinine',
        'sodium': 'Sodium',
        'potassium': 'Potassium',
        'hemoglobin': 'Hemoglobin',
        'bun': 'BUN',
        'egfr': 'eGFR',
        'acr': 'ACR',
        'ucr': 'UCR',
        
        # CKD Stages
        'no_ckd': 'No CKD',
        'stage_1': 'Stage 1',
        'stage_2': 'Stage 2',
        'stage_3': 'Stage 3',
        'stage_4': 'Stage 4',
        'stage_5': 'Stage 5',
        
        # Prediction Results
        'ckd_detected': 'CKD Detected',
        'no_ckd_detected': 'No CKD Detected',
        'confidence_score': 'Confidence Score',
        'risk_level': 'Risk Level',
        'low_risk': 'Low Risk',
        'medium_risk': 'Medium Risk',
        'high_risk': 'High Risk',
        
        # Recommendations
        'diet_plan': 'Diet Plan',
        'exercise_plan': 'Exercise Plan',
        'lifestyle_tips': 'Lifestyle Tips',
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'dinner': 'Dinner',
        'snacks': 'Snacks',
        'daily_activity': 'Daily Activity',
        'frequency': 'Frequency',
        'intensity': 'Intensity',
        'duration': 'Duration',
        'precautions': 'Precautions',
        'benefits': 'Benefits',
        
        # Dashboard
        'welcome': 'Welcome',
        'recent_predictions': 'Recent Predictions',
        'health_summary': 'Health Summary',
        'recommendations': 'Recommendations',
        'ai_assistant': 'AI Assistant',
        'chat_with_ai': 'Chat with AI',
        'send_message': 'Send Message',
        'type_message': 'Type your message...',
        
        # Doctor Dashboard
        'analytics': 'Analytics',
        'total_patients': 'Total Patients',
        'ckd_patients': 'CKD Patients',
        'non_ckd_patients': 'Non-CKD Patients',
        'total_predictions': 'Total Predictions',
        'model_accuracy': 'Model Accuracy',
        'stage_distribution': 'Stage Distribution',
        'recent_activity': 'Recent Activity',
        
        # Reports
        'generate_report': 'Generate Report',
        'download_report': 'Download Report',
        'send_email': 'Send Email',
        'print_report': 'Print Report',
        'report_generated': 'Report Generated',
        'email_sent': 'Email Sent',
        
        # Common Actions
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'view': 'View',
        'download': 'Download',
        'upload': 'Upload',
        'search': 'Search',
        'filter': 'Filter',
        'sort': 'Sort',
        'refresh': 'Refresh',
        
        # Messages
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Information',
        'loading': 'Loading...',
        'please_wait': 'Please wait...',
        'operation_successful': 'Operation successful',
        'operation_failed': 'Operation failed',
        'invalid_input': 'Invalid input',
        'required_field': 'This field is required',
        
        # Homepage
        'hero_title': 'Smart CKD Health Management',
        'hero_subtitle': 'AI-powered Chronic Kidney Disease detection and personalized health management system.',
        'get_started': 'Get Started',
        'key_features': 'Key Features',
        'features_subtitle': 'Comprehensive CKD management with cutting-edge AI technology',
        'ai_detection': 'AI-Powered Detection',
        'ai_detection_desc': 'Advanced machine learning algorithms with 98% accuracy for CKD prediction using Random Forest model.',
        'diet_plans': 'Personalized Diet Plans',
        'diet_plans_desc': 'Stage-specific diet recommendations tailored to your CKD condition and health requirements.',
        'exercise_recommendations': 'Exercise Recommendations',
        'exercise_recommendations_desc': 'Customized exercise plans based on your CKD stage and physical condition.',
        'ai_assistant_feature': 'AI Health Assistant',
        'ai_assistant_feature_desc': '24/7 AI chatbot powered by Gemini for health queries and guidance in English and Kannada.',
        'doctor_analytics': 'Doctor Analytics',
        'doctor_analytics_desc': 'Comprehensive analytics dashboard for healthcare providers to monitor patient progress.',
        'automated_reports': 'Automated Reports',
        'automated_reports_desc': 'Generate and email detailed health reports with predictions and recommendations.',
        'technology_stack': 'Technology Stack',
        'tech_subtitle': 'Built with modern technologies for optimal performance',
        'ready_to_start': 'Ready to Get Started?',
        'cta_subtitle': 'Join thousands of patients and doctors using our Smart CKD Health Management system.',
        'signup_patient': 'Sign Up as Patient',
        'signup_doctor': 'Sign Up as Doctor',
        
        # Login Page
        'welcome_back': 'Welcome Back',
        'sign_in_message': 'Sign in to your account',
        'i_am_a': 'I am a:',
        'sign_in': 'Sign In',
        'no_account': "Don't have an account?",
        'sign_up_here': 'Sign up here',
        
        # Dashboard Elements
        'overview': 'Overview',
        'new_prediction': 'New Prediction',
        'prediction_history': 'Prediction History',
        'welcome_patient': 'Welcome, Patient!',
        'total_predictions': 'Total Predictions',
        'healthy': 'Healthy',
        'current_status': 'Current Status',
        'member_since': 'Member Since',
        'active': 'Active',
        'notifications': 'Notifications',
        'recent_predictions': 'Recent Predictions',
        'date': 'Date',
        'ckd_status': 'CKD Status',
        'stage': 'Stage',
        'confidence': 'Confidence',
        'risk_level': 'Risk Level',
        'no_predictions_yet': 'No predictions yet',
        'start_prediction': 'Start by making your first CKD prediction!',
        'make_prediction': 'Make Prediction',
        'ckd_prediction': 'CKD Prediction',
        'back_to_overview': 'Back to Overview',
        'enter_health_parameters': 'Enter Health Parameters',
        'prediction_results': 'Prediction Results',
        'submit_form_message': 'Submit the form to see prediction results',
        'select_gender': 'Select Gender',
        'male': 'Male',
        'female': 'Female',
        'predict_ckd_status': 'Predict CKD Status',
        'health_recommendations': 'Health Recommendations',
        'diet_plan': 'Diet Plan',
        'exercise_plan': 'Exercise Plan',
        'lifestyle_tips': 'Lifestyle Tips',
        'no_recommendations': 'No recommendations available',
        'chat_with_ai': 'Chat with AI Assistant',
        'type_message_here': 'Type your message here...',
        'quick_questions': 'Quick Questions',
        'ckd_symptoms': 'What are the symptoms of CKD?',
        'avoid_foods': 'What foods should I avoid with CKD?',
        'prevent_progression': 'How can I prevent CKD progression?',
        'safe_exercises': 'What exercises are safe for CKD patients?',
        'full_name': 'Full Name',
        'phone_number': 'Phone Number',
        'create_account': 'Create Account',
        'join_system': 'Join our Smart CKD Health Management system',
        'password_requirements': 'Password must be at least 8 characters long.',
        'agree_terms': 'I agree to the Terms of Service and Privacy Policy',
        'terms_of_service': 'Terms of Service',
        'privacy_policy': 'Privacy Policy',
        'already_have_account': 'Already have an account?',
        'sign_in_here': 'Sign in here',
        
        # Additional translations found in templates
        'personalized_diet_plans': 'Personalized Diet Plans',
        'personalized_diet_plans_desc': 'Stage-specific diet recommendations tailored to your CKD condition and health requirements.',
        'exercise_recommendations': 'Exercise Recommendations',
        'exercise_recommendations_desc': 'Customized exercise plans based on your CKD stage and physical condition.',
        'ai_health_assistant': 'AI Health Assistant',
        'ai_health_assistant_desc': '24/7 AI chatbot powered by Gemini for health queries and guidance in English and Kannada.',
        'doctor_analytics': 'Doctor Analytics',
        'doctor_analytics_desc': 'Comprehensive analytics dashboard for healthcare providers to monitor patient progress.',
        'automated_reports': 'Automated Reports',
        'automated_reports_desc': 'Generate and email detailed health reports with predictions and recommendations.',
        'technology_stack': 'Technology Stack',
        'tech_subtitle': 'Built with modern technologies for optimal performance',
        'python_flask': 'Python & Flask',
        'backend_framework': 'Backend Framework',
        'mongodb': 'MongoDB',
        'database': 'Database',
        'scikit_learn': 'Scikit-learn',
        'machine_learning': 'Machine Learning',
        'gemini_ai': 'Gemini AI',
        'ai_assistant': 'AI Assistant',
        'ready_to_get_started': 'Ready to Get Started?',
        'join_thousands': 'Join thousands of patients and doctors using our Smart CKD Health Management system.',
        'sign_up_as_patient': 'Sign Up as Patient',
        'sign_up_as_doctor': 'Sign Up as Doctor',
        'email_address': 'Email Address',
        'password_requirements': 'Password must be at least 8 characters long.',
        'agree_terms': 'I agree to the Terms of Service and Privacy Policy',
        'terms_of_service': 'Terms of Service',
        'privacy_policy': 'Privacy Policy',
        'normal_case': 'Normal Case',
        'ckd_case': 'CKD Case',
        'severe_ckd': 'Severe CKD',
        'prediction_history': 'Prediction History',
        'no_prediction_history': 'No prediction history',
        'make_first_prediction': 'Make your first prediction to see history here.',
        'actions': 'Actions',
        'report': 'Report',
        'health_recommendations': 'Health Recommendations',
        'ckd_stage': 'CKD Stage',
        'no_recommendations_available': 'No recommendations available',
        'make_prediction_to_get_recommendations': 'Make a prediction to get personalized recommendations.',
        'chat_with_ai_assistant': 'Chat with AI Assistant',
        'powered_by_gemini': 'Powered by Gemini AI',
        'hello_ai_assistant': 'Hello! I\'m your AI health assistant. How can I help you with CKD-related questions or general health advice?',
        'type_your_message_here': 'Type your message here...',
        'quick_questions': 'Quick Questions',
        'what_are_ckd_symptoms': 'What are the symptoms of CKD?',
        'what_foods_avoid_ckd': 'What foods should I avoid with CKD?',
        'how_prevent_ckd_progression': 'How can I prevent CKD progression?',
        'what_exercises_safe_ckd': 'What exercises are safe for CKD patients?',
        'fluid_intake': 'Fluid Intake',
        'sodium_limit': 'Sodium Limit',
        'protein_intake': 'Protein Intake',
        'restrictions': 'Restrictions',
        'glasses_water_daily': '8-10 glasses of water daily',
        'less_than_2000mg': 'Less than 2,000mg per day',
        'protein_per_kg': '0.8g per kg body weight',
        'reduce_sodium_limit_processed': 'Reduce sodium, limit processed foods',
        'minutes_per_session': '25-30 minutes per session',
        'monitor_bp_stay_hydrated': 'Monitor blood pressure, stay hydrated',
        'maintains_kidney_function': 'Maintains kidney function, improves overall health',
        'lifestyle_tips': 'Lifestyle Tips',
        'stay_hydrated_appropriate': 'Stay hydrated with appropriate fluid intake',
        'monitor_bp_regularly': 'Monitor blood pressure regularly',
        'follow_medication_schedule': 'Follow prescribed medication schedule',
        'maintain_regular_followups': 'Maintain regular follow-ups with healthcare provider',
        'age_range': 'Age (Range: 20-90)',
        'gender': 'Gender',
        'blood_pressure_range': 'Blood Pressure (mmHg) (Range: 80-200)',
        'sugar_level_range': 'Sugar Level (mg/dL) (Range: 70-300)',
        'albumin_range': 'Albumin (g/dL) (Range: 1.0-5.0)',
        'serum_creatinine_range': 'Serum Creatinine (mg/dL) (Range: 0.5-10.0)',
        'sodium_range': 'Sodium (mEq/L) (Range: 120-160)',
        'potassium_range': 'Potassium (mEq/L) (Range: 2.0-6.0)',
        'hemoglobin_range': 'Hemoglobin (g/dL) (Range: 8-18)',
        'bun_range': 'BUN (mg/dL) (Range: 5-50)',
        'egfr_range': 'eGFR (mL/min/1.73m²) (Range: 10-120)',
        'acr_range': 'ACR (mg/g) (Range: 0-500)',
        'ucr_range': 'UCR (mg/g) (Range: 0-50)',
        'select_gender': 'Select Gender',
        'male': 'Male',
        'female': 'Female',
        'normal_case': 'Normal Case',
        'ckd_case': 'CKD Case',
        'severe_ckd': 'Severe CKD',
        'predict_ckd_status': 'Predict CKD Status',
        'prediction_results': 'Prediction Results',
        'submit_form_message': 'Submit the form to see prediction results',
        'prediction_history': 'Prediction History',
        'no_prediction_history': 'No prediction history',
        'make_first_prediction': 'Make your first prediction to see history here.',
        'actions': 'Actions',
        'report': 'Report',
        'health_recommendations': 'Health Recommendations',
        'ckd_stage': 'CKD Stage',
        'no_recommendations_available': 'No recommendations available',
        'make_prediction_to_get_recommendations': 'Make a prediction to get personalized recommendations.',
        'chat_with_ai_assistant': 'Chat with AI Assistant',
        'powered_by_gemini': 'Powered by Gemini AI',
        'hello_ai_assistant': 'Hello! I\'m your AI health assistant. How can I help you with CKD-related questions or general health advice?',
        'type_your_message_here': 'Type your message here...',
        'quick_questions': 'Quick Questions',
        'what_are_ckd_symptoms': 'What are the symptoms of CKD?',
        'what_foods_avoid_ckd': 'What foods should I avoid with CKD?',
        'how_prevent_ckd_progression': 'How can I prevent CKD progression?',
        'what_exercises_safe_ckd': 'What exercises are safe for CKD patients?',
        'invalid_credentials': 'Invalid credentials',
        'patient_exists': 'Patient with this email already exists',
        'doctor_exists': 'Doctor with this email already exists',
        'messages': 'Messages',
        'health_trends': 'Health Trends',
        'last_30_days': 'Last 30 Days',
        'last_90_days': 'Last 90 Days',
        'last_year': 'Last Year',
        'refresh': 'Refresh',
        'messages_from_doctor': 'Messages from Doctor',
        'loading_messages': 'Loading messages...',
        'egfr_trend': 'eGFR Trend',
        'risk_alerts': 'Risk Alerts',
        'loading_alerts': 'Loading alerts...',
        'blood_pressure_trend': 'Blood Pressure Trend',
        'acr_trend': 'ACR Trend',
    },
    
    'kn': {
        # App Info
        'app_name': 'ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ',
        'app_description': 'ಎಐ-ಚಾಲಿತ ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ ಪತ್ತೆ ಮತ್ತು ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ.',
        'copyright': '© 2025 ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ. ಎಲ್ಲ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
        
        # Navigation
        'home': 'ಮುಖಪುಟ',
        'dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'login': 'ಲಾಗಿನ್',
        'signup': 'ಸೈನ್ ಅಪ್',
        'logout': 'ಲಾಗ್‌ಔಟ್',
        'profile': 'ಪ್ರೊಫೈಲ್',
        'settings': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
        
        # Authentication
        'email': 'ಇಮೇಲ್',
        'password': 'ಪಾಸ್‌ವರ್ಡ್',
        'confirm_password': 'ಪಾಸ್‌ವರ್ಡ್ ದೃಢೀಕರಿಸಿ',
        'name': 'ಹೆಸರು',
        'phone': 'ಫೋನ್',
        'user_type': 'ಬಳಕೆದಾರ ಪ್ರಕಾರ',
        'patient': 'ರೋಗಿ',
        'doctor': 'ವೈದ್ಯ',
        'sign_in': 'ಸೈನ್ ಇನ್',
        'create_account': 'ಖಾತೆ ರಚಿಸಿ',
        'forgot_password': 'ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?',
        
        # Health Parameters
        'age': 'ವಯಸ್ಸು',
        'gender': 'ಲಿಂಗ',
        'blood_pressure': 'ರಕ್ತದೊತ್ತಡ',
        'sugar_level': 'ಸಕ್ಕರೆ ಮಟ್ಟ',
        'albumin': 'ಆಲ್ಬುಮಿನ್',
        'serum_creatinine': 'ಸೀರಮ್ ಕ್ರಿಯಾಟಿನಿನ್',
        'sodium': 'ಸೋಡಿಯಂ',
        'potassium': 'ಪೊಟ್ಯಾಸಿಯಂ',
        'hemoglobin': 'ಹೀಮೋಗ್ಲೋಬಿನ್',
        'bun': 'ಬಿಇಎನ್',
        'egfr': 'ಇಜಿಎಫ್ಆರ್',
        'acr': 'ಎಸಿಆರ್',
        'ucr': 'ಯುಸಿಆರ್',
        
        # CKD Stages
        'no_ckd': 'ಸಿಕೆಡಿ ಇಲ್ಲ',
        'stage_1': 'ಹಂತ 1',
        'stage_2': 'ಹಂತ 2',
        'stage_3': 'ಹಂತ 3',
        'stage_4': 'ಹಂತ 4',
        'stage_5': 'ಹಂತ 5',
        
        # Prediction Results
        'ckd_detected': 'ಸಿಕೆಡಿ ಪತ್ತೆಯಾಗಿದೆ',
        'no_ckd_detected': 'ಸಿಕೆಡಿ ಪತ್ತೆಯಾಗಿಲ್ಲ',
        'confidence_score': 'ನಂಬಿಕೆ ಸ್ಕೋರ್',
        'risk_level': 'ಅಪಾಯ ಮಟ್ಟ',
        'low_risk': 'ಕಡಿಮೆ ಅಪಾಯ',
        'medium_risk': 'ಮಧ್ಯಮ ಅಪಾಯ',
        'high_risk': 'ಹೆಚ್ಚಿನ ಅಪಾಯ',
        
        # Recommendations
        'diet_plan': 'ಆಹಾರ ಯೋಜನೆ',
        'exercise_plan': 'ವ್ಯಾಯಾಮ ಯೋಜನೆ',
        'lifestyle_tips': 'ಜೀವನಶೈಲಿ ಸಲಹೆಗಳು',
        'breakfast': 'ಉಪಹಾರ',
        'lunch': 'ಊಟ',
        'dinner': 'ಅಡುಗೆ',
        'snacks': 'ತಿಂಡಿ',
        'daily_activity': 'ದೈನಂದಿನ ಚಟುವಟಿಕೆ',
        'frequency': 'ಆವರ್ತನೆ',
        'intensity': 'ತೀವ್ರತೆ',
        'duration': 'ಅವಧಿ',
        'precautions': 'ಎಚ್ಚರಿಕೆಗಳು',
        'benefits': 'ಪ್ರಯೋಜನಗಳು',
        
        # Dashboard
        'welcome': 'ಸ್ವಾಗತ',
        'recent_predictions': 'ಇತ್ತೀಚಿನ ಭವಿಷ್ಯವಾಣಿಗಳು',
        'health_summary': 'ಆರೋಗ್ಯ ಸಾರಾಂಶ',
        'recommendations': 'ಶಿಫಾರಸುಗಳು',
        'ai_assistant': 'ಎಐ ಸಹಾಯಕ',
        'chat_with_ai': 'ಎಐ ಜೊತೆ ಚಾಟ್ ಮಾಡಿ',
        'send_message': 'ಸಂದೇಶ ಕಳುಹಿಸಿ',
        'type_message': 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಟೈಪ್ ಮಾಡಿ...',
        
        # Doctor Dashboard
        'analytics': 'ವಿಶ್ಲೇಷಣೆ',
        'total_patients': 'ಒಟ್ಟು ರೋಗಿಗಳು',
        'ckd_patients': 'ಸಿಕೆಡಿ ರೋಗಿಗಳು',
        'non_ckd_patients': 'ಸಿಕೆಡಿ ರೋಗಿಗಳಲ್ಲದವರು',
        'total_predictions': 'ಒಟ್ಟು ಭವಿಷ್ಯವಾಣಿಗಳು',
        'model_accuracy': 'ಮಾದರಿ ನಿಖರತೆ',
        'stage_distribution': 'ಹಂತ ವಿತರಣೆ',
        'recent_activity': 'ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ',
        
        # Reports
        'generate_report': 'ರಿಪೋರ್ಟ್ ರಚಿಸಿ',
        'download_report': 'ರಿಪೋರ್ಟ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ',
        'send_email': 'ಇಮೇಲ್ ಕಳುಹಿಸಿ',
        'print_report': 'ರಿಪೋರ್ಟ್ ಮುದ್ರಿಸಿ',
        'report_generated': 'ರಿಪೋರ್ಟ್ ರಚಿಸಲಾಗಿದೆ',
        'email_sent': 'ಇಮೇಲ್ ಕಳುಹಿಸಲಾಗಿದೆ',
        
        # Common Actions
        'submit': 'ಸಲ್ಲಿಸಿ',
        'cancel': 'ರದ್ದುಗೊಳಿಸಿ',
        'save': 'ಉಳಿಸಿ',
        'edit': 'ಸಂಪಾದಿಸಿ',
        'delete': 'ಅಳಿಸಿ',
        'view': 'ನೋಡಿ',
        'download': 'ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ',
        'upload': 'ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'search': 'ಹುಡುಕಿ',
        'filter': 'ಫಿಲ್ಟರ್ ಮಾಡಿ',
        'sort': 'ವಿಂಗಡಿಸಿ',
        'refresh': 'ರಿಫ್ರೆಶ್ ಮಾಡಿ',
        
        # Messages
        'success': 'ಯಶಸ್ಸು',
        'error': 'ದೋಷ',
        'warning': 'ಎಚ್ಚರಿಕೆ',
        'info': 'ಮಾಹಿತಿ',
        'loading': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
        'please_wait': 'ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...',
        'operation_successful': 'ಕಾರ್ಯಾಚರಣೆ ಯಶಸ್ವಿಯಾಗಿದೆ',
        'operation_failed': 'ಕಾರ್ಯಾಚರಣೆ ವಿಫಲವಾಗಿದೆ',
        'invalid_input': 'ಅಮಾನ್ಯ ಇನ್‌ಪುಟ್',
        'required_field': 'ಈ ಕ್ಷೇತ್ರ ಅಗತ್ಯವಾಗಿದೆ',
        
        # Health Tips
        'stay_hydrated': 'ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯುವ ಮೂಲಕ ಜಲಯುಕ್ತವಾಗಿರಿ',
        'monitor_bp': 'ರಕ್ತದೊತ್ತಡವನ್ನು ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ',
        'follow_medication': 'ನಿರ್ದಿಷ್ಟಪಡಿಸಿದ ಔಷಧಿ ವೇಳಾಪಟ್ಟಿಯನ್ನು ಅನುಸರಿಸಿ',
        'regular_checkups': 'ಆರೋಗ್ಯ ಸೇವಾ ಒದಗಿಸುವವರೊಂದಿಗೆ ನಿಯಮಿತ ಫಾಲೋ-ಅಪ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ',
        'healthy_diet': 'ಸಾಕಷ್ಟು ಹಣ್ಣುಗಳು ಮತ್ತು ತರಕಾರಿಗಳೊಂದಿಗೆ ಸಮತೋಲಿತ ಆಹಾರವನ್ನು ತಿನ್ನಿ',
        'regular_exercise': 'ನಿಯಮಿತ ವ್ಯಾಯಾಮ ಮಾಡಿ',
        'avoid_smoking': 'ಧೂಮಪಾನ ಮತ್ತು ತಂಬಾಕು ಉತ್ಪನ್ನಗಳನ್ನು ತಪ್ಪಿಸಿ',
        'limit_alcohol': 'ಮದ್ಯ ಸೇವನೆಯನ್ನು ಸೀಮಿತಗೊಳಿಸಿ',
        
        # Homepage
        'hero_title': 'ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ನಿರ್ವಹಣೆ',
        'hero_subtitle': 'ಎಐ-ಚಾಲಿತ ಕ್ರಾನಿಕ್ ಕಿಡ್ನಿ ರೋಗ ಪತ್ತೆ ಮತ್ತು ವೈಯಕ್ತಿಕ ಆರೋಗ್ಯ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ.',
        'get_started': 'ಪ್ರಾರಂಭಿಸಿ',
        'key_features': 'ಮುಖ್ಯ ವೈಶಿಷ್ಟ್ಯಗಳು',
        'features_subtitle': 'ಆಧುನಿಕ ಎಐ ತಂತ್ರಜ್ಞಾನದೊಂದಿಗೆ ಸಮಗ್ರ ಸಿಕೆಡಿ ನಿರ್ವಹಣೆ',
        'ai_detection': 'ಎಐ-ಚಾಲಿತ ಪತ್ತೆ',
        'ai_detection_desc': 'ರ್ಯಾಂಡಮ್ ಫಾರೆಸ್ಟ್ ಮಾದರಿಯನ್ನು ಬಳಸಿಕೊಂಡು ಸಿಕೆಡಿ ಭವಿಷ್ಯವಾಣಿಗೆ 98% ನಿಖರತೆಯೊಂದಿಗೆ ಸುಧಾರಿತ ಯಂತ್ರ ಕಲಿಕೆ ಅಲ್ಗಾರಿದಮ್‌ಗಳು.',
        'diet_plans': 'ವೈಯಕ್ತಿಕ ಆಹಾರ ಯೋಜನೆಗಳು',
        'diet_plans_desc': 'ನಿಮ್ಮ ಸಿಕೆಡಿ ಸ್ಥಿತಿ ಮತ್ತು ಆರೋಗ್ಯ ಅಗತ್ಯಗಳಿಗೆ ಹೊಂದಿಕೊಂಡ ಹಂತ-ನಿರ್ದಿಷ್ಟ ಆಹಾರ ಶಿಫಾರಸುಗಳು.',
        'exercise_recommendations': 'ವ್ಯಾಯಾಮ ಶಿಫಾರಸುಗಳು',
        'exercise_recommendations_desc': 'ನಿಮ್ಮ ಸಿಕೆಡಿ ಹಂತ ಮತ್ತು ದೈಹಿಕ ಸ್ಥಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಕಸ್ಟಮೈಸ್ ಮಾಡಿದ ವ್ಯಾಯಾಮ ಯೋಜನೆಗಳು.',
        'ai_assistant_feature': 'ಎಐ ಆರೋಗ್ಯ ಸಹಾಯಕ',
        'ai_assistant_feature_desc': 'ಆರೋಗ್ಯ ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ಇಂಗ್ಲಿಷ್ ಮತ್ತು ಕನ್ನಡದಲ್ಲಿ ಜೆಮಿನಿ ಚಾಲಿತ 24/7 ಎಐ ಚಾಟ್‌ಬಾಟ್.',
        'doctor_analytics': 'ವೈದ್ಯ ವಿಶ್ಲೇಷಣೆ',
        'doctor_analytics_desc': 'ರೋಗಿಯ ಪ್ರಗತಿಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಲು ಆರೋಗ್ಯ ಸೇವಾ ಒದಗಿಸುವವರಿಗೆ ಸಮಗ್ರ ವಿಶ್ಲೇಷಣೆ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್.',
        'automated_reports': 'ಸ್ವಯಂಚಾಲಿತ ವರದಿಗಳು',
        'automated_reports_desc': 'ಭವಿಷ್ಯವಾಣಿಗಳು ಮತ್ತು ಶಿಫಾರಸುಗಳೊಂದಿಗೆ ವಿವರವಾದ ಆರೋಗ್ಯ ವರದಿಗಳನ್ನು ರಚಿಸಿ ಮತ್ತು ಇಮೇಲ್ ಮಾಡಿ.',
        'technology_stack': 'ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್',
        'tech_subtitle': 'ಸೂಕ್ತ ಕಾರ್ಯಕ್ಷಮತೆಗಾಗಿ ಆಧುನಿಕ ತಂತ್ರಜ್ಞಾನಗಳೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾಗಿದೆ',
        'ready_to_start': 'ಪ್ರಾರಂಭಿಸಲು ಸಿದ್ಧರಾಗಿದ್ದೀರಾ?',
        'cta_subtitle': 'ನಮ್ಮ ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆಯನ್ನು ಬಳಸುವ ಸಾವಿರಾರು ರೋಗಿಗಳು ಮತ್ತು ವೈದ್ಯರೊಂದಿಗೆ ಸೇರಿ.',
        'signup_patient': 'ರೋಗಿಯಾಗಿ ಸೈನ್ ಅಪ್ ಮಾಡಿ',
        'signup_doctor': 'ವೈದ್ಯರಾಗಿ ಸೈನ್ ಅಪ್ ಮಾಡಿ',
        
        # Login Page
        'welcome_back': 'ಮತ್ತೆ ಸ್ವಾಗತ',
        'sign_in_message': 'ನಿಮ್ಮ ಖಾತೆಗೆ ಸೈನ್ ಇನ್ ಮಾಡಿ',
        'i_am_a': 'ನಾನು ಒಬ್ಬ:',
        'sign_in': 'ಸೈನ್ ಇನ್',
        'no_account': 'ಖಾತೆ ಇಲ್ಲವೇ?',
        'sign_up_here': 'ಇಲ್ಲಿ ಸೈನ್ ಅಪ್ ಮಾಡಿ',
        
        # Dashboard Elements
        'overview': 'ಅವಲೋಕನ',
        'new_prediction': 'ಹೊಸ ಭವಿಷ್ಯವಾಣಿ',
        'prediction_history': 'ಭವಿಷ್ಯವಾಣಿ ಇತಿಹಾಸ',
        'welcome_patient': 'ಸ್ವಾಗತ, ರೋಗಿ!',
        'total_predictions': 'ಒಟ್ಟು ಭವಿಷ್ಯವಾಣಿಗಳು',
        'healthy': 'ಆರೋಗ್ಯವಂತ',
        'current_status': 'ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ',
        'member_since': 'ಸದಸ್ಯರಾದ ದಿನಾಂಕ',
        'active': 'ಸಕ್ರಿಯ',
        'notifications': 'ಅಧಿಸೂಚನೆಗಳು',
        'recent_predictions': 'ಇತ್ತೀಚಿನ ಭವಿಷ್ಯವಾಣಿಗಳು',
        'date': 'ದಿನಾಂಕ',
        'ckd_status': 'ಸಿಕೆಡಿ ಸ್ಥಿತಿ',
        'stage': 'ಹಂತ',
        'confidence': 'ನಂಬಿಕೆ',
        'risk_level': 'ಅಪಾಯ ಮಟ್ಟ',
        'no_predictions_yet': 'ಇನ್ನೂ ಭವಿಷ್ಯವಾಣಿಗಳಿಲ್ಲ',
        'start_prediction': 'ನಿಮ್ಮ ಮೊದಲ ಸಿಕೆಡಿ ಭವಿಷ್ಯವಾಣಿಯನ್ನು ಮಾಡುವ ಮೂಲಕ ಪ್ರಾರಂಭಿಸಿ!',
        'make_prediction': 'ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ',
        'ckd_prediction': 'ಸಿಕೆಡಿ ಭವಿಷ್ಯವಾಣಿ',
        'back_to_overview': 'ಅವಲೋಕನಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'enter_health_parameters': 'ಆರೋಗ್ಯ ನಿಯತಾಂಕಗಳನ್ನು ನಮೂದಿಸಿ',
        'prediction_results': 'ಭವಿಷ್ಯವಾಣಿ ಫಲಿತಾಂಶಗಳು',
        'submit_form_message': 'ಭವಿಷ್ಯವಾಣಿ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಲು ಫಾರ್ಮ್ ಅನ್ನು ಸಲ್ಲಿಸಿ',
        'select_gender': 'ಲಿಂಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'male': 'ಪುರುಷ',
        'female': 'ಸ್ತ್ರೀ',
        'predict_ckd_status': 'ಸಿಕೆಡಿ ಸ್ಥಿತಿಯನ್ನು ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ',
        'health_recommendations': 'ಆರೋಗ್ಯ ಶಿಫಾರಸುಗಳು',
        'diet_plan': 'ಆಹಾರ ಯೋಜನೆ',
        'exercise_plan': 'ವ್ಯಾಯಾಮ ಯೋಜನೆ',
        'lifestyle_tips': 'ಜೀವನಶೈಲಿ ಸಲಹೆಗಳು',
        'no_recommendations': 'ಶಿಫಾರಸುಗಳು ಲಭ್ಯವಿಲ್ಲ',
        'chat_with_ai': 'ಎಐ ಸಹಾಯಕ ಜೊತೆ ಚಾಟ್ ಮಾಡಿ',
        'type_message_here': 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'quick_questions': 'ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು',
        'ckd_symptoms': 'ಸಿಕೆಡಿಯ ಲಕ್ಷಣಗಳು ಯಾವುವು?',
        'avoid_foods': 'ಸಿಕೆಡಿಯೊಂದಿಗೆ ನಾನು ಯಾವ ಆಹಾರಗಳನ್ನು ತಪ್ಪಿಸಬೇಕು?',
        'prevent_progression': 'ನಾನು ಸಿಕೆಡಿ ಪ್ರಗತಿಯನ್ನು ಹೇಗೆ ತಡೆಗಟ್ಟಬಹುದು?',
        'safe_exercises': 'ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ ಯಾವ ವ್ಯಾಯಾಮಗಳು ಸುರಕ್ಷಿತ?',
        'full_name': 'ಪೂರ್ಣ ಹೆಸರು',
        'phone_number': 'ಫೋನ್ ಸಂಖ್ಯೆ',
        'create_account': 'ಖಾತೆ ರಚಿಸಿ',
        'join_system': 'ನಮ್ಮ ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆಗೆ ಸೇರಿ',
        'password_requirements': 'ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 8 ಅಕ್ಷರಗಳು ಇರಬೇಕು.',
        'agree_terms': 'ನಾನು ಸೇವಾ ನಿಯಮಗಳು ಮತ್ತು ಗೌಪ್ಯತೆ ನೀತಿಗೆ ಒಪ್ಪುತ್ತೇನೆ',
        'terms_of_service': 'ಸೇವಾ ನಿಯಮಗಳು',
        'privacy_policy': 'ಗೌಪ್ಯತೆ ನೀತಿ',
        'already_have_account': 'ಈಗಾಗಲೇ ಖಾತೆ ಇದೆಯೇ?',
        'sign_in_here': 'ಇಲ್ಲಿ ಸೈನ್ ಇನ್ ಮಾಡಿ',
        
        # Additional translations found in templates
        'personalized_diet_plans': 'ವೈಯಕ್ತಿಕಗೊಳಿಸಿದ ಆಹಾರ ಯೋಜನೆಗಳು',
        'personalized_diet_plans_desc': 'ನಿಮ್ಮ CKD ಸ್ಥಿತಿ ಮತ್ತು ಆರೋಗ್ಯದ ಅವಶ್ಯಕತೆಗಳಿಗೆ ಅನುಗುಣವಾಗಿ ಹಂತ-ನಿರ್ದಿಷ್ಟ ಆಹಾರ ಶಿಫಾರಸುಗಳು.',
        'exercise_recommendations': 'ವ್ಯಾಯಾಮ ಶಿಫಾರಸುಗಳು',
        'exercise_recommendations_desc': 'ನಿಮ್ಮ CKD ಹಂತ ಮತ್ತು ದೈಹಿಕ ಸ್ಥಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಕಸ್ಟಮೈಸ್ ಮಾಡಿದ ವ್ಯಾಯಾಮ ಯೋಜನೆಗಳು.',
        'ai_health_assistant': 'AI ಆರೋಗ್ಯ ಸಹಾಯಕ',
        'ai_health_assistant_desc': 'ಆರೋಗ್ಯ ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ಜೆಮಿನಿ ಚಾಲಿತ 24/7 AI ಚಾಟ್‌ಬಾಟ್ ಇಂಗ್ಲಿಷ್ ಮತ್ತು ಕನ್ನಡದಲ್ಲಿ ಲಭ್ಯವಿದೆ.',
        'doctor_analytics': 'ವೈದ್ಯರ ವಿಶ್ಲೇಷಣೆಗಳು',
        'doctor_analytics_desc': 'ಆರೋಗ್ಯ ಸೇವೆ ಒದಗಿಸುವವರಿಗೆ ರೋಗಿಯ ಪ್ರಗತಿಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಲು ಸಮಗ್ರ ವಿಶ್ಲೇಷಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್.',
        'automated_reports': 'ಸ್ವಯಂಚಾಲಿತ ವರದಿಗಳು',
        'automated_reports_desc': 'ಭವಿಷ್ಯವಾಣಿಗಳು ಮತ್ತು ಶಿಫಾರಸುಗಳೊಂದಿಗೆ ವಿವರವಾದ ಆರೋಗ್ಯ ವರದಿಗಳನ್ನು ರಚಿಸಿ ಮತ್ತು ಇಮೇಲ್ ಮಾಡಿ.',
        'technology_stack': 'ತಂತ್ರಜ್ಞಾನ ಸ್ಟಾಕ್',
        'tech_subtitle': 'ಸೂಕ್ತ ಕಾರ್ಯಕ್ಷಮತೆಗಾಗಿ ಆಧುನಿಕ ತಂತ್ರಜ್ಞಾನಗಳೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾಗಿದೆ',
        'python_flask': 'Python & Flask',
        'backend_framework': 'ಬ್ಯಾಕ್‌ಎಂಡ್ ಫ್ರೇಮ್‌ವರ್ಕ್',
        'mongodb': 'MongoDB',
        'database': 'ಡೇಟಾಬೇಸ್',
        'scikit_learn': 'Scikit-learn',
        'machine_learning': 'ಯಂತ್ರ ಕಲಿಕೆ',
        'gemini_ai': 'Gemini AI',
        'ai_assistant': 'AI ಸಹಾಯಕ',
        'ready_to_get_started': 'ಪ್ರಾರಂಭಿಸಲು ಸಿದ್ಧರಾಗಿದ್ದೀರಾ?',
        'join_thousands': 'ನಮ್ಮ ಸ್ಮಾರ್ಟ್ ಸಿಕೆಡಿ ಆರೋಗ್ಯ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆಯನ್ನು ಬಳಸುವ ಸಾವಿರಾರು ರೋಗಿಗಳು ಮತ್ತು ವೈದ್ಯರೊಂದಿಗೆ ಸೇರಿ.',
        'sign_up_as_patient': 'ರೋಗಿಯಾಗಿ ಸೈನ್ ಅಪ್ ಮಾಡಿ',
        'sign_up_as_doctor': 'ವೈದ್ಯರಾಗಿ ಸೈನ್ ಅಪ್ ಮಾಡಿ',
        'email_address': 'ಇಮೇಲ್ ವಿಳಾಸ',
        'password_requirements': 'ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 8 ಅಕ್ಷರಗಳು ಇರಬೇಕು.',
        'agree_terms': 'ನಾನು ಸೇವಾ ನಿಯಮಗಳು ಮತ್ತು ಗೌಪ್ಯತೆ ನೀತಿಗೆ ಒಪ್ಪುತ್ತೇನೆ',
        'terms_of_service': 'ಸೇವಾ ನಿಯಮಗಳು',
        'privacy_policy': 'ಗೌಪ್ಯತೆ ನೀತಿ',
        'normal_case': 'ಸಾಮಾನ್ಯ ಪ್ರಕರಣ',
        'ckd_case': 'CKD ಪ್ರಕರಣ',
        'severe_ckd': 'ತೀವ್ರ CKD',
        'prediction_history': 'ಭವಿಷ್ಯವಾಣಿ ಇತಿಹಾಸ',
        'no_prediction_history': 'ಭವಿಷ್ಯವಾಣಿ ಇತಿಹಾಸವಿಲ್ಲ',
        'make_first_prediction': 'ಇತಿಹಾಸವನ್ನು ನೋಡಲು ನಿಮ್ಮ ಮೊದಲ ಭವಿಷ್ಯವಾಣಿಯನ್ನು ಮಾಡಿ.',
        'actions': 'ಕ್ರಿಯೆಗಳು',
        'report': 'ವರದಿ',
        'health_recommendations': 'ಆರೋಗ್ಯ ಶಿಫಾರಸುಗಳು',
        'ckd_stage': 'CKD ಹಂತ',
        'no_recommendations_available': 'ಶಿಫಾರಸುಗಳು ಲಭ್ಯವಿಲ್ಲ',
        'make_prediction_to_get_recommendations': 'ವೈಯಕ್ತಿಕ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಲು ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ.',
        'chat_with_ai_assistant': 'AI ಸಹಾಯಕ ಜೊತೆ ಚಾಟ್ ಮಾಡಿ',
        'powered_by_gemini': 'Gemini AI ಚಾಲಿತ',
        'hello_ai_assistant': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ AI ಆರೋಗ್ಯ ಸಹಾಯಕ. ಸಿಕೆಡಿ-ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳು ಅಥವಾ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?',
        'type_your_message_here': 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'quick_questions': 'ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು',
        'what_are_ckd_symptoms': 'ಸಿಕೆಡಿಯ ಲಕ್ಷಣಗಳು ಯಾವುವು?',
        'what_foods_avoid_ckd': 'ಸಿಕೆಡಿಯೊಂದಿಗೆ ನಾನು ಯಾವ ಆಹಾರಗಳನ್ನು ತಪ್ಪಿಸಬೇಕು?',
        'how_prevent_ckd_progression': 'ನಾನು ಸಿಕೆಡಿ ಪ್ರಗತಿಯನ್ನು ಹೇಗೆ ತಡೆಗಟ್ಟಬಹುದು?',
        'what_exercises_safe_ckd': 'ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ ಯಾವ ವ್ಯಾಯಾಮಗಳು ಸುರಕ್ಷಿತ?',
        'fluid_intake': 'ದ್ರವ ಸೇವನೆ',
        'sodium_limit': 'ಸೋಡಿಯಂ ಮಿತಿ',
        'protein_intake': 'ಪ್ರೋಟೀನ್ ಸೇವನೆ',
        'restrictions': 'ನಿರ್ಬಂಧಗಳು',
        'glasses_water_daily': 'ದಿನಕ್ಕೆ 8-10 ಗ್ಲಾಸ್ ನೀರು',
        'less_than_2000mg': 'ದಿನಕ್ಕೆ 2,000mg ಗಿಂತ ಕಡಿಮೆ',
        'protein_per_kg': 'ಕೆಜಿ ದೇಹ ತೂಕಕ್ಕೆ 0.8g',
        'reduce_sodium_limit_processed': 'ಸೋಡಿಯಂ ಕಡಿಮೆ ಮಾಡಿ, ಸಂಸ್ಕರಿಸಿದ ಆಹಾರಗಳನ್ನು ಸೀಮಿತಗೊಳಿಸಿ',
        'minutes_per_session': 'ಅಧಿವೇಶನಕ್ಕೆ 25-30 ನಿಮಿಷಗಳು',
        'monitor_bp_stay_hydrated': 'ರಕ್ತದೊತ್ತಡವನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ, ಜಲಯುಕ್ತವಾಗಿರಿ',
        'maintains_kidney_function': 'ಮೂತ್ರಪಿಂಡ ಕಾರ್ಯವನ್ನು ನಿರ್ವಹಿಸುತ್ತದೆ, ಒಟ್ಟಾರೆ ಆರೋಗ್ಯವನ್ನು ಸುಧಾರಿಸುತ್ತದೆ',
        'lifestyle_tips': 'ಜೀವನಶೈಲಿ ಸಲಹೆಗಳು',
        'stay_hydrated_appropriate': 'ಸೂಕ್ತ ದ್ರವ ಸೇವನೆಯೊಂದಿಗೆ ಜಲಯುಕ್ತವಾಗಿರಿ',
        'monitor_bp_regularly': 'ರಕ್ತದೊತ್ತಡವನ್ನು ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ',
        'follow_medication_schedule': 'ನಿರ್ದಿಷ್ಟಪಡಿಸಿದ ಔಷಧಿ ವೇಳಾಪಟ್ಟಿಯನ್ನು ಅನುಸರಿಸಿ',
        'maintain_regular_followups': 'ಆರೋಗ್ಯ ಸೇವೆ ಒದಗಿಸುವವರೊಂದಿಗೆ ನಿಯಮಿತ ಫಾಲೋ-ಅಪ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ',
        'age_range': 'ವಯಸ್ಸು (ಶ್ರೇಣಿ: 20-90)',
        'gender': 'ಲಿಂಗ',
        'blood_pressure_range': 'ರಕ್ತದೊತ್ತಡ (mmHg) (ಶ್ರೇಣಿ: 80-200)',
        'sugar_level_range': 'ಸಕ್ಕರೆ ಮಟ್ಟ (mg/dL) (ಶ್ರೇಣಿ: 70-300)',
        'albumin_range': 'ಅಲ್ಬುಮಿನ್ (g/dL) (ಶ್ರೇಣಿ: 1.0-5.0)',
        'serum_creatinine_range': 'ಸೀರಮ್ ಕ್ರಿಯೇಟಿನೈನ್ (mg/dL) (ಶ್ರೇಣಿ: 0.5-10.0)',
        'sodium_range': 'ಸೋಡಿಯಂ (mEq/L) (ಶ್ರೇಣಿ: 120-160)',
        'potassium_range': 'ಪೊಟ್ಯಾಸಿಯಮ್ (mEq/L) (ಶ್ರೇಣಿ: 2.0-6.0)',
        'hemoglobin_range': 'ಹಿಮೋಗ್ಲೋಬಿನ್ (g/dL) (ಶ್ರೇಣಿ: 8-18)',
        'bun_range': 'BUN (mg/dL) (ಶ್ರೇಣಿ: 5-50)',
        'egfr_range': 'eGFR (mL/min/1.73m²) (ಶ್ರೇಣಿ: 10-120)',
        'acr_range': 'ACR (mg/g) (ಶ್ರೇಣಿ: 0-500)',
        'ucr_range': 'UCR (mg/g) (ಶ್ರೇಣಿ: 0-50)',
        'select_gender': 'ಲಿಂಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'male': 'ಪುರುಷ',
        'female': 'ಸ್ತ್ರೀ',
        'normal_case': 'ಸಾಮಾನ್ಯ ಪ್ರಕರಣ',
        'ckd_case': 'CKD ಪ್ರಕರಣ',
        'severe_ckd': 'ತೀವ್ರ CKD',
        'predict_ckd_status': 'ಸಿಕೆಡಿ ಸ್ಥಿತಿಯನ್ನು ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ',
        'prediction_results': 'ಭವಿಷ್ಯವಾಣಿ ಫಲಿತಾಂಶಗಳು',
        'submit_form_message': 'ಭವಿಷ್ಯವಾಣಿ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಲು ಫಾರ್ಮ್ ಅನ್ನು ಸಲ್ಲಿಸಿ',
        'prediction_history': 'ಭವಿಷ್ಯವಾಣಿ ಇತಿಹಾಸ',
        'no_prediction_history': 'ಭವಿಷ್ಯವಾಣಿ ಇತಿಹಾಸವಿಲ್ಲ',
        'make_first_prediction': 'ಇತಿಹಾಸವನ್ನು ನೋಡಲು ನಿಮ್ಮ ಮೊದಲ ಭವಿಷ್ಯವಾಣಿಯನ್ನು ಮಾಡಿ.',
        'actions': 'ಕ್ರಿಯೆಗಳು',
        'report': 'ವರದಿ',
        'health_recommendations': 'ಆರೋಗ್ಯ ಶಿಫಾರಸುಗಳು',
        'ckd_stage': 'CKD ಹಂತ',
        'no_recommendations_available': 'ಶಿಫಾರಸುಗಳು ಲಭ್ಯವಿಲ್ಲ',
        'make_prediction_to_get_recommendations': 'ವೈಯಕ್ತಿಕ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಲು ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ.',
        'chat_with_ai_assistant': 'AI ಸಹಾಯಕ ಜೊತೆ ಚಾಟ್ ಮಾಡಿ',
        'powered_by_gemini': 'Gemini AI ಚಾಲಿತ',
        'hello_ai_assistant': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ AI ಆರೋಗ್ಯ ಸಹಾಯಕ. ಸಿಕೆಡಿ-ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳು ಅಥವಾ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಲಹೆಗಳ ಬಗ್ಗೆ ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?',
        'type_your_message_here': 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'quick_questions': 'ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು',
        'what_are_ckd_symptoms': 'ಸಿಕೆಡಿಯ ಲಕ್ಷಣಗಳು ಯಾವುವು?',
        'what_foods_avoid_ckd': 'ಸಿಕೆಡಿಯೊಂದಿಗೆ ನಾನು ಯಾವ ಆಹಾರಗಳನ್ನು ತಪ್ಪಿಸಬೇಕು?',
        'how_prevent_ckd_progression': 'ನಾನು ಸಿಕೆಡಿ ಪ್ರಗತಿಯನ್ನು ಹೇಗೆ ತಡೆಗಟ್ಟಬಹುದು?',
        'what_exercises_safe_ckd': 'ಸಿಕೆಡಿ ರೋಗಿಗಳಿಗೆ ಯಾವ ವ್ಯಾಯಾಮಗಳು ಸುರಕ್ಷಿತ?',
        'invalid_credentials': 'ಅಮಾನ್ಯ ದೃಢೀಕರಣಗಳು',
        'patient_exists': 'ಈ ಇಮೇಲ್‌ನೊಂದಿಗೆ ರೋಗಿ ಈಗಾಗಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿದೆ',
        'doctor_exists': 'ಈ ಇಮೇಲ್‌ನೊಂದಿಗೆ ವೈದ್ಯ ಈಗಾಗಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿದೆ',
        'messages': 'ಸಂದೇಶಗಳು',
        'health_trends': 'ಆರೋಗ್ಯ ಪ್ರವೃತ್ತಿಗಳು',
        'last_30_days': 'ಕಳೆದ 30 ದಿನಗಳು',
        'last_90_days': 'ಕಳೆದ 90 ದಿನಗಳು',
        'last_year': 'ಕಳೆದ ವರ್ಷ',
        'refresh': 'ರಿಫ್ರೆಶ್ ಮಾಡಿ',
        'messages_from_doctor': 'ವೈದ್ಯರಿಂದ ಸಂದೇಶಗಳು',
        'loading_messages': 'ಸಂದೇಶಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        'egfr_trend': 'eGFR ಪ್ರವೃತ್ತಿ',
        'risk_alerts': 'ಅಪಾಯ ಎಚ್ಚರಿಕೆಗಳು',
        'loading_alerts': 'ಎಚ್ಚರಿಕೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        'blood_pressure_trend': 'ರಕ್ತದೊತ್ತಡ ಪ್ರವೃತ್ತಿ',
        'acr_trend': 'ACR ಪ್ರವೃತ್ತಿ',
    }
}

def get_translation(key, language='en'):
    """
    Get translation for a given key in the specified language
    
    Args:
        key (str): Translation key
        language (str): Language code ('en' or 'kn')
    
    Returns:
        str: Translated text or original key if translation not found
    """
    if language not in TRANSLATIONS:
        language = 'en'  # Default to English
    
    return TRANSLATIONS[language].get(key, key)

def get_all_translations(language='en'):
    """
    Get all translations for a specific language
    
    Args:
        language (str): Language code ('en' or 'kn')
    
    Returns:
        dict: All translations for the language
    """
    if language not in TRANSLATIONS:
        language = 'en'  # Default to English
    
    return TRANSLATIONS[language]

def translate_text(text, from_lang='en', to_lang='kn'):
    """
    Simple translation function (placeholder for more advanced translation)
    In a real implementation, you would use Google Translate API or similar
    
    Args:
        text (str): Text to translate
        from_lang (str): Source language
        to_lang (str): Target language
    
    Returns:
        str: Translated text
    """
    # This is a simple mapping - in production, use proper translation API
    if to_lang == 'kn':
        # Simple English to Kannada mapping for common terms
        simple_translations = {
            'Welcome': 'ಸ್ವಾಗತ',
            'Login': 'ಲಾಗಿನ್',
            'Sign Up': 'ಸೈನ್ ಅಪ್',
            'Dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
            'Patient': 'ರೋಗಿ',
            'Doctor': 'ವೈದ್ಯ',
            'Health': 'ಆರೋಗ್ಯ',
            'Report': 'ರಿಪೋರ್ಟ್',
            'Settings': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
            'Logout': 'ಲಾಗ್‌ಔಟ್'
        }
        return simple_translations.get(text, text)
    else:
        return text

def get_language_name(language_code):
    """
    Get the full name of a language from its code
    
    Args:
        language_code (str): Language code ('en' or 'kn')
    
    Returns:
        str: Full language name
    """
    language_names = {
        'en': 'English',
        'kn': 'ಕನ್ನಡ (Kannada)'
    }
    return language_names.get(language_code, 'English')

def get_supported_languages():
    """
    Get list of supported languages
    
    Returns:
        list: List of supported language codes
    """
    return list(TRANSLATIONS.keys())

def create_language_switcher_html():
    """
    Create HTML for language switcher dropdown
    
    Returns:
        str: HTML for language switcher
    """
    html = '''
    <div class="language-switcher">
        <select id="languageSelect" onchange="switchLanguage(this.value)">
            <option value="en">English</option>
            <option value="kn">ಕನ್ನಡ</option>
        </select>
    </div>
    '''
    return html

def create_language_switcher_js():
    """
    Create JavaScript for language switching functionality
    
    Returns:
        str: JavaScript code for language switching
    """
    js = '''
    function switchLanguage(language) {
        // Store language preference
        localStorage.setItem('preferred_language', language);
        
        // Update page content
        updatePageLanguage(language);
        
        // Send AJAX request to update server-side language
        fetch('/api/set-language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({language: language})
        });
    }
    
    function updatePageLanguage(language) {
        // Update all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            element.textContent = getTranslation(key, language);
        });
        
        // Update form placeholders
        document.querySelectorAll('[data-placeholder]').forEach(element => {
            const key = element.getAttribute('data-placeholder');
            element.placeholder = getTranslation(key, language);
        });
    }
    
    function getTranslation(key, language) {
        // This would typically fetch from the server
        // For now, return the key as placeholder
        return key;
    }
    
    // Load saved language preference
    document.addEventListener('DOMContentLoaded', function() {
        const savedLanguage = localStorage.getItem('preferred_language') || 'en';
        document.getElementById('languageSelect').value = savedLanguage;
        updatePageLanguage(savedLanguage);
    });
    '''
    return js

# Test functions
def test_translations():
    """Test the translation system"""
    print("=== Testing Multilingual Support ===\n")
    
    # Test English translations
    print("English Translations:")
    test_keys = ['home', 'login', 'patient', 'doctor', 'dashboard']
    for key in test_keys:
        translation = get_translation(key, 'en')
        print(f"  {key}: {translation}")
    
    print("\nKannada Translations:")
    for key in test_keys:
        translation = get_translation(key, 'kn')
        print(f"  {key}: {translation}")
    
    # Test language names
    print(f"\nSupported Languages:")
    for lang_code in get_supported_languages():
        lang_name = get_language_name(lang_code)
        print(f"  {lang_code}: {lang_name}")

if __name__ == "__main__":
    test_translations()
