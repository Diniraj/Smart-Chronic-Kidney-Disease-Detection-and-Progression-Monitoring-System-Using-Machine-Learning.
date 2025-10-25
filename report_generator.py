# PDF Report Generation and Email Delivery System

"""
This module implements comprehensive PDF report generation and email delivery for the Smart CKD Health Management System.
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import json
import uuid
from io import BytesIO
import base64

# PDF Generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

# Email functionality
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Database connection
from pymongo import MongoClient

print("Report generation system initialized successfully!")

# Configuration and Database Setup
# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['ckd_health_management']

# Email configuration (read from environment variables when available)
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', '587')),
    'email_user': os.environ.get('GMAIL_USER', 'your-email@gmail.com'),
    'email_password': os.environ.get('GMAIL_PASS', 'your-app-password'),
    'from_name': os.environ.get('FROM_NAME', 'Smart CKD Health Management System')
}

# Log basic email config (safe)
try:
    masked = EMAIL_CONFIG['email_user'][:2] + '***' if EMAIL_CONFIG['email_user'] else 'not set'
    print(f"Email config → server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}, user: {masked}")
except Exception:
    pass

# Report configuration
REPORT_CONFIG = {
    'company_name': 'Smart CKD Health Management',
    'company_address': 'Healthcare Technology Solutions',
    'company_phone': '+91-9876543210',
    'company_email': 'info@smartckd.com',
    'website': 'www.smartckd.com'
}

print("Configuration loaded successfully!")

# PDF Report Generation Functions
def create_patient_report(prediction_id, patient_id=None):
    """
    Generate comprehensive PDF report for a patient prediction
    """
    try:
        # Get prediction data
        prediction = db.predictions.find_one({"prediction_id": prediction_id})
        if not prediction:
            return None, "Prediction not found"
        
        # Get patient data
        if patient_id:
            patient = db.patients.find_one({"patient_id": patient_id})
        else:
            patient = db.patients.find_one({"patient_id": prediction['patient_id']})
        
        # Debug logging
        print(f"DEBUG: Patient found: {patient is not None}")
        if patient:
            print(f"DEBUG: Patient age: {patient['personal_info'].get('age')}")
            print(f"DEBUG: Patient gender: {patient['personal_info'].get('gender')}")
            print(f"DEBUG: Patient name: {patient['personal_info'].get('name')}")
        
        # Get recommendations
        recommendation = db.recommendations.find_one({"patient_id": prediction['patient_id']})
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Header
        story.append(Paragraph("Smart CKD Health Management System", title_style))
        story.append(Paragraph("Comprehensive Health Report", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Patient Information
        if patient:
            story.append(Paragraph("Patient Information", heading_style))
            patient_info = [
                ['Name:', patient['personal_info']['name']],
                ['Email:', patient['personal_info']['email']],
                ['Phone:', patient['personal_info']['phone']],
                ['Age:', str(patient['personal_info']['age']) if patient['personal_info']['age'] else 'N/A'],
                ['Gender:', patient['personal_info']['gender']],
                ['Report Date:', datetime.now().strftime('%B %d, %Y')]
            ]
            
            patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ]))
            story.append(patient_table)
            story.append(Spacer(1, 20))
        
        # Prediction Results
        story.append(Paragraph("CKD Prediction Results", heading_style))
        result = prediction['prediction_result']
        
        # Risk level color coding
        risk_color = colors.red if result['risk_level'] == 'High' else colors.orange if result['risk_level'] == 'Medium' else colors.green
        
        prediction_data = [
            ['CKD Status:', 'CKD Detected' if result['ckd_binary'] else 'No CKD'],
            ['CKD Stage:', result['ckd_stage']],
            ['Confidence Score:', f"{result['confidence']:.2%}"],
            ['Risk Level:', result['risk_level']],
            ['Model Used:', prediction['model_used']],
            ['Prediction Date:', prediction['created_at'].strftime('%B %d, %Y at %I:%M %p')]
        ]
        
        prediction_table = Table(prediction_data, colWidths=[2*inch, 4*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('TEXTCOLOR', (1, 2), (1, 2), risk_color),  # Risk level color
        ]))
        story.append(prediction_table)
        story.append(Spacer(1, 20))
        
        # Health Parameters
        story.append(Paragraph("Health Parameters", heading_style))
        input_data = prediction['input_data']
        print(f"Debug: input_data keys: {list(input_data.keys())}")
        print(f"Debug: input_data values: {input_data}")
        
        # Get blood pressure values (stored as single value in Blood_Pressure)
        blood_pressure_value = input_data.get('Blood_Pressure', 'N/A')
        blood_pressure_str = str(blood_pressure_value) if blood_pressure_value != 'N/A' else 'N/A'
        
        health_params = [
            ['Parameter', 'Value', 'Normal Range'],
            ['Age', str(input_data.get('age', 'N/A')), 'N/A'],
            ['Gender', 'M' if input_data.get('gender_M', 0) == 1 else 'F', 'M/F'],
            ['Blood Pressure (mmHg)', blood_pressure_str, '< 140/90'],
            ['Sugar Level (mg/dL)', str(input_data.get('Sugar_Level', 'N/A')), '< 126'],
            ['Albumin (g/dL)', str(input_data.get('Albumin', 'N/A')), '3.5-5.0'],
            ['Serum Creatinine (mg/dL)', str(input_data.get('Serum_Creatinine', 'N/A')), '0.6-1.2'],
            ['Sodium (mEq/L)', str(input_data.get('Sodium', 'N/A')), '136-145'],
            ['Potassium (mEq/L)', str(input_data.get('Potassium', 'N/A')), '3.5-5.0'],
            ['Hemoglobin (g/dL)', str(input_data.get('Hemoglobin', 'N/A')), '12-16'],
            ['BUN (mg/dL)', str(input_data.get('BUN', 'N/A')), '7-20'],
            ['eGFR (mL/min/1.73m²)', str(input_data.get('eGFR', 'N/A')), '> 90'],
            ['ACR (mg/g)', str(input_data.get('ACR', 'N/A')), '< 30'],
            ['UCR (mg/g)', str(input_data.get('UCR', 'N/A')), 'N/A']
        ]
        
        health_table = Table(health_params, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        health_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(health_table)
        story.append(Spacer(1, 20))
        
        # Recommendations
        if recommendation:
            story.append(Paragraph("Personalized Recommendations", heading_style))
            
            # Diet Plan
            story.append(Paragraph("Diet Plan", styles['Heading3']))
            diet_plan = recommendation['diet_plan']
            diet_items = [
                ['Meal', 'Recommendation'],
                ['Breakfast', diet_plan.get('breakfast', 'N/A')],
                ['Lunch', diet_plan.get('lunch', 'N/A')],
                ['Dinner', diet_plan.get('dinner', 'N/A')],
                ['Snacks', diet_plan.get('snacks', 'N/A')]
            ]
            
            diet_table = Table(diet_items, colWidths=[1.5*inch, 4.5*inch])
            diet_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(diet_table)
            story.append(Spacer(1, 12))
            
            # Exercise Plan
            story.append(Paragraph("Exercise Plan", styles['Heading3']))
            exercise_plan = recommendation['exercise_plan']
            exercise_items = [
                ['Aspect', 'Recommendation'],
                ['Daily Activity', exercise_plan.get('daily_activity', 'N/A')],
                ['Frequency', exercise_plan.get('frequency', 'N/A')],
                ['Intensity', exercise_plan.get('intensity', 'N/A')],
                ['Recommended Exercises', ', '.join(exercise_plan.get('recommended_exercises', []))]
            ]
            
            exercise_table = Table(exercise_items, colWidths=[1.5*inch, 4.5*inch])
            exercise_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(exercise_table)
            story.append(Spacer(1, 12))
            
            # Lifestyle Tips
            story.append(Paragraph("Lifestyle Tips", styles['Heading3']))
            for i, tip in enumerate(recommendation['lifestyle_tips'], 1):
                story.append(Paragraph(f"{i}. {tip}", styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Footer
        story.append(Spacer(1, 20))
        story.append(Paragraph("This report was generated by Smart CKD Health Management System", styles['Normal']))
        story.append(Paragraph(f"Report ID: {prediction_id}", styles['Normal']))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue(), None
        
    except Exception as e:
        return None, str(e)

# Email Delivery Functions
def send_email_report(recipient_email, recipient_name, pdf_content, prediction_id):
    """
    Send PDF report via email
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['email_user']}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"CKD Health Report - {prediction_id}"
        
        # Email body
        body = f"""
Dear {recipient_name},

Please find attached your comprehensive CKD health report generated by our Smart CKD Health Management System.

Report Details:
- Report ID: {prediction_id}
- Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
- System: Smart CKD Health Management

This report contains:
✓ Your health parameters analysis
✓ CKD prediction results with confidence scores
✓ Personalized diet and exercise recommendations
✓ Lifestyle tips for better health management

Please consult with your healthcare provider regarding any concerns or questions about this report.

Best regards,
Smart CKD Health Management Team
{REPORT_CONFIG['company_name']}
{REPORT_CONFIG['company_email']}
{REPORT_CONFIG['company_phone']}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        pdf_attachment = MIMEBase('application', 'octet-stream')
        pdf_attachment.set_payload(pdf_content)
        encoders.encode_base64(pdf_attachment)
        pdf_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= "CKD_Health_Report_{prediction_id}.pdf"'
        )
        msg.attach(pdf_attachment)
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email_user'], EMAIL_CONFIG['email_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email_user'], recipient_email, text)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, str(e)

def send_sms_notification(phone_number, message):
    """
    Send SMS notification (placeholder for Twilio integration)
    """
    try:
        # This is a placeholder - you would integrate with Twilio here
        # For now, we'll just log the message
        print(f"SMS to {phone_number}: {message}")
        return True, "SMS notification sent"
    except Exception as e:
        return False, str(e)

# Complete Report Generation and Delivery System
def generate_and_send_report(prediction_id, patient_id=None, send_email=True, send_sms=True):
    """
    Complete workflow: Generate PDF report and send via email/SMS
    """
    try:
        # Generate PDF report
        pdf_content, error = create_patient_report(prediction_id, patient_id)
        if error:
            return False, f"PDF generation failed: {error}"
        
        # Get patient information
        if patient_id:
            patient = db.patients.find_one({"patient_id": patient_id})
        else:
            prediction = db.predictions.find_one({"prediction_id": prediction_id})
            patient = db.patients.find_one({"patient_id": prediction['patient_id']})
        
        if not patient:
            return False, "Patient not found"
        
        # Send email if requested
        if send_email:
            email_success, email_message = send_email_report(
                patient['personal_info']['email'],
                patient['personal_info']['name'],
                pdf_content,
                prediction_id
            )
            if not email_success:
                print(f"Email sending failed: {email_message}")
        
        # Send SMS if requested
        if send_sms:
            sms_message = f"Your CKD health report (ID: {prediction_id}) has been generated and sent to your email. Please check your inbox."
            sms_success, sms_message_result = send_sms_notification(
                patient['personal_info']['phone'],
                sms_message
            )
            if not sms_success:
                print(f"SMS sending failed: {sms_message_result}")
        
        # Save report to database
        report_data = {
            "report_id": f"RPT_{str(uuid.uuid4())[:8]}",
            "prediction_id": prediction_id,
            "patient_id": patient['patient_id'],
            "report_type": "comprehensive_health_report",
            "email_sent": send_email,
            "sms_sent": send_sms,
            "created_at": datetime.now(),
            "file_size": len(pdf_content)
        }
        
        db.reports.insert_one(report_data)
        
        return True, "Report generated and delivered successfully"
        
    except Exception as e:
        return False, str(e)

# Batch report generation for multiple patients
def generate_batch_reports(patient_ids, send_emails=True, send_sms=True):
    """
    Generate reports for multiple patients
    """
    results = []
    
    for patient_id in patient_ids:
        # Get latest prediction for this patient
        prediction = db.predictions.find_one(
            {"patient_id": patient_id},
            sort=[("created_at", -1)]
        )
        
        if prediction:
            success, message = generate_and_send_report(
                prediction['prediction_id'],
                patient_id,
                send_emails,
                send_sms
            )
            results.append({
                'patient_id': patient_id,
                'prediction_id': prediction['prediction_id'],
                'success': success,
                'message': message
            })
        else:
            results.append({
                'patient_id': patient_id,
                'prediction_id': None,
                'success': False,
                'message': 'No prediction found'
            })
    
    return results

# Test functions
def test_report_generation():
    """Test the report generation system"""
    print("=== Testing Report Generation System ===\n")
    
    # Get a sample prediction to test with
    sample_prediction = db.predictions.find_one({})
    if sample_prediction:
        prediction_id = sample_prediction['prediction_id']
        patient_id = sample_prediction['patient_id']
        
        print(f"Testing with prediction ID: {prediction_id}")
        print(f"Patient ID: {patient_id}")
        
        # Test PDF generation (without sending email/SMS)
        print("\n1. Testing PDF generation...")
        pdf_content, error = create_patient_report(prediction_id, patient_id)
        
        if error:
            print(f"[FAIL] PDF generation failed: {error}")
        else:
            print(f"[PASS] PDF generated successfully! Size: {len(pdf_content)} bytes")
            
            # Save test PDF to file
            with open(f"test_report_{prediction_id}.pdf", "wb") as f:
                f.write(pdf_content)
            print(f"[INFO] Test PDF saved as: test_report_{prediction_id}.pdf")
        
        # Test complete workflow (without actual email/SMS sending)
        print("\n2. Testing complete workflow...")
        success, message = generate_and_send_report(
            prediction_id, 
            patient_id, 
            send_email=False,  # Don't actually send email
            send_sms=False     # Don't actually send SMS
        )
        
        if success:
            print(f"[PASS] Complete workflow successful: {message}")
        else:
            print(f"[FAIL] Complete workflow failed: {message}")
            
    else:
        print("[FAIL] No predictions found in database. Please run database_setup.ipynb first.")
    
    print("\n=== Report Generation System Test Complete ===")

def test_email_configuration():
    """Test email configuration"""
    print("=== Testing Email Configuration ===")
    print(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
    print(f"SMTP Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"Email User: {EMAIL_CONFIG['email_user']}")
    print(f"From Name: {EMAIL_CONFIG['from_name']}")
    print("\nNote: Update EMAIL_CONFIG with your actual email credentials to test email sending.")

def test_database_connection():
    """Test database connection"""
    print("=== Testing Database Connection ===")
    try:
        # Test connection
        client.admin.command('ping')
        print("[PASS] MongoDB connection successful!")
        
        # Check collections
        collections = db.list_collection_names()
        print(f"Available collections: {collections}")
        
        # Check sample data
        patient_count = db.patients.count_documents({})
        prediction_count = db.predictions.count_documents({})
        recommendation_count = db.recommendations.count_documents({})
        
        print(f"Patients: {patient_count}")
        print(f"Predictions: {prediction_count}")
        print(f"Recommendations: {recommendation_count}")
        
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")

if __name__ == "__main__":
    print("=== Testing Report Generation System ===\n")
    
    # Test database connection
    print("1. Testing Database Connection:")
    test_database_connection()
    
    # Test email configuration
    print("\n2. Testing Email Configuration:")
    test_email_configuration()
    
    # Test report generation
    print("\n3. Testing Report Generation:")
    test_report_generation()
    
    print("\n=== All Tests Complete ===")
