# Diet & Exercise Recommendation Engine

"""
This module implements the recommendation system for CKD patients based on their stage and health condition.
"""

# Import required libraries
import pandas as pd
import numpy as np
import json
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configure Gemini AI from environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    print("Warning: GEMINI_API_KEY is not set. Gemini features will be disabled in recommendations.")
    model = None

print("Recommendation Engine initialized successfully!")

# Stage-based Diet Plans
def get_diet_plan(ckd_stage, age=None, gender=None):
    """
    Generate diet plan based on CKD stage
    """
    diet_plans = {
        'No CKD': {
            'breakfast': 'Oatmeal with fresh fruits and low-fat milk',
            'lunch': 'Grilled chicken breast with brown rice and steamed vegetables',
            'dinner': 'Baked fish with quinoa and mixed salad',
            'snacks': 'Mixed nuts, Greek yogurt, fresh fruits',
            'fluid_intake': '8-10 glasses of water daily',
            'sodium_limit': 'Less than 2,300mg per day',
            'protein_intake': '0.8-1.0g per kg body weight',
            'restrictions': 'Limit processed foods, maintain balanced diet'
        },
        'Stage 1': {
            'breakfast': 'Whole grain toast with avocado and fresh fruit',
            'lunch': 'Lean protein (chicken/fish) with vegetables and brown rice',
            'dinner': 'Baked fish with sweet potato and steamed broccoli',
            'snacks': 'Apple slices, unsalted nuts, fresh berries',
            'fluid_intake': '8-10 glasses of water daily',
            'sodium_limit': 'Less than 2,000mg per day',
            'protein_intake': '0.8g per kg body weight',
            'restrictions': 'Reduce sodium, limit processed foods'
        },
        'Stage 2': {
            'breakfast': 'Low-sodium cereal with almond milk and berries',
            'lunch': 'Grilled chicken salad with olive oil dressing',
            'dinner': 'Baked salmon with steamed vegetables and white rice',
            'snacks': 'Fresh berries, low-sodium crackers, unsalted nuts',
            'fluid_intake': '6-8 glasses of water daily',
            'sodium_limit': 'Less than 1,500mg per day',
            'protein_intake': '0.8g per kg body weight',
            'restrictions': 'Low sodium, moderate protein, avoid high phosphorus foods'
        },
        'Stage 3': {
            'breakfast': 'Low-phosphorus bread with jam and fresh fruit',
            'lunch': 'Turkey sandwich on low-sodium bread with vegetables',
            'dinner': 'Baked cod with white rice and steamed vegetables',
            'snacks': 'Fresh fruits, low-sodium pretzels, rice cakes',
            'fluid_intake': '6-8 glasses of water daily',
            'sodium_limit': 'Less than 1,500mg per day',
            'protein_intake': '0.6-0.8g per kg body weight',
            'restrictions': 'Low sodium, low phosphorus, moderate protein'
        },
        'Stage 4': {
            'breakfast': 'Low-potassium fruits with toast and jam',
            'lunch': 'Chicken breast with white rice and low-potassium vegetables',
            'dinner': 'Baked white fish with pasta and steamed vegetables',
            'snacks': 'Low-potassium vegetables, rice cakes',
            'fluid_intake': '4-6 glasses of water daily',
            'sodium_limit': 'Less than 1,000mg per day',
            'protein_intake': '0.6g per kg body weight',
            'restrictions': 'Low sodium, low potassium, low phosphorus, fluid restriction'
        },
        'Stage 5': {
            'breakfast': 'Low-phosphorus, low-potassium breakfast options',
            'lunch': 'Dialysis-friendly meal plan with controlled portions',
            'dinner': 'Renal diet approved foods with strict portion control',
            'snacks': 'Dialysis center approved snacks only',
            'fluid_intake': 'As prescribed by doctor (usually 1-1.5L daily)',
            'sodium_limit': 'Less than 1,000mg per day',
            'protein_intake': 'As prescribed by doctor',
            'restrictions': 'Strict fluid restriction, low sodium, low potassium, low phosphorus'
        }
    }
    
    return diet_plans.get(ckd_stage, diet_plans['No CKD'])

# Stage-based Exercise Plans
def get_exercise_plan(ckd_stage, age=None, gender=None):
    """
    Generate exercise plan based on CKD stage and patient characteristics
    """
    exercise_plans = {
        'No CKD': {
            'daily_activity': '30 minutes of moderate exercise',
            'recommended_exercises': ['Walking', 'Swimming', 'Cycling', 'Yoga', 'Dancing'],
            'frequency': '5-6 days per week',
            'intensity': 'Moderate (can talk but not sing)',
            'duration': '30-45 minutes per session',
            'precautions': 'Stay hydrated, listen to your body',
            'benefits': 'Improves cardiovascular health, maintains healthy weight'
        },
        'Stage 1': {
            'daily_activity': '25-30 minutes of light to moderate exercise',
            'recommended_exercises': ['Walking', 'Swimming', 'Light yoga', 'Tai chi'],
            'frequency': '4-5 days per week',
            'intensity': 'Light to Moderate',
            'duration': '25-30 minutes per session',
            'precautions': 'Monitor blood pressure, stay hydrated',
            'benefits': 'Maintains kidney function, improves overall health'
        },
        'Stage 2': {
            'daily_activity': '20-25 minutes of light exercise',
            'recommended_exercises': ['Walking', 'Stretching', 'Gentle yoga', 'Chair exercises'],
            'frequency': '3-4 days per week',
            'intensity': 'Light',
            'duration': '20-25 minutes per session',
            'precautions': 'Avoid high-impact activities, monitor symptoms',
            'benefits': 'Maintains mobility, reduces fatigue'
        },
        'Stage 3': {
            'daily_activity': '15-20 minutes of gentle exercise',
            'recommended_exercises': ['Walking', 'Stretching', 'Breathing exercises', 'Chair yoga'],
            'frequency': '3 days per week',
            'intensity': 'Very Light',
            'duration': '15-20 minutes per session',
            'precautions': 'Stop if feeling tired or short of breath',
            'benefits': 'Maintains strength, improves quality of life'
        },
        'Stage 4': {
            'daily_activity': '10-15 minutes of very gentle movement',
            'recommended_exercises': ['Walking', 'Chair exercises', 'Breathing exercises', 'Light stretching'],
            'frequency': '2-3 days per week',
            'intensity': 'Very Light',
            'duration': '10-15 minutes per session',
            'precautions': 'Consult doctor before starting, stop if uncomfortable',
            'benefits': 'Maintains basic mobility, reduces stiffness'
        },
        'Stage 5': {
            'daily_activity': '5-10 minutes of gentle movement',
            'recommended_exercises': ['Chair exercises', 'Breathing exercises', 'Light stretching', 'Range of motion'],
            'frequency': 'As tolerated',
            'intensity': 'Minimal',
            'duration': '5-10 minutes per session',
            'precautions': 'Only with doctor approval, stop if any discomfort',
            'benefits': 'Maintains joint mobility, improves circulation'
        }
    }
    
    return exercise_plans.get(ckd_stage, exercise_plans['No CKD'])

# Gemini AI Integration for Personalized Recommendations
def get_gemini_recommendations(ckd_stage, age, gender, specific_concerns=None, language='en'):
    """
    Get personalized recommendations using Gemini AI
    """
    try:
        # Create context-aware prompt
        prompt = f"""
        You are a healthcare AI assistant specializing in Chronic Kidney Disease (CKD) management.
        
        Patient Profile:
        - CKD Stage: {ckd_stage}
        - Age: {age}
        - Gender: {gender}
        - Language: {language}
        - Specific Concerns: {specific_concerns or 'None'}
        
        Please provide personalized health recommendations focusing on:
        1. Diet and nutrition advice specific to their CKD stage
        2. Safe exercise recommendations
        3. Lifestyle modifications
        4. Warning signs to watch for
        5. When to consult a doctor
        
        Respond in {language} language and be empathetic and encouraging.
        Keep recommendations practical and easy to follow.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I encountered an error generating personalized recommendations: {str(e)}"

def generate_lifestyle_tips(ckd_stage):
    """
    Generate lifestyle tips based on CKD stage
    """
    tips_by_stage = {
        'No CKD': [
            "Maintain a healthy weight",
            "Stay hydrated with adequate water intake",
            "Monitor blood pressure regularly",
            "Limit alcohol consumption",
            "Avoid smoking and tobacco products",
            "Get regular exercise",
            "Eat a balanced diet with plenty of fruits and vegetables"
        ],
        'Stage 1': [
            "Monitor kidney function regularly",
            "Control blood pressure and blood sugar",
            "Stay hydrated but don't overdo it",
            "Limit sodium intake",
            "Avoid NSAIDs unless prescribed",
            "Get regular check-ups with your doctor",
            "Maintain a healthy lifestyle"
        ],
        'Stage 2': [
            "Work closely with your healthcare team",
            "Monitor symptoms and report changes",
            "Follow a kidney-friendly diet",
            "Stay active but avoid overexertion",
            "Take medications as prescribed",
            "Limit phosphorus and potassium if needed",
            "Stay informed about your condition"
        ],
        'Stage 3': [
            "Regular monitoring of kidney function",
            "Strict adherence to dietary restrictions",
            "Fluid restriction may be necessary",
            "Avoid high-phosphorus foods",
            "Monitor for symptoms of kidney failure",
            "Consider seeing a nephrologist",
            "Plan for potential dialysis or transplant"
        ],
        'Stage 4': [
            "Prepare for kidney replacement therapy",
            "Strict fluid and diet restrictions",
            "Regular monitoring of symptoms",
            "Avoid activities that could cause injury",
            "Stay in close contact with healthcare team",
            "Consider dialysis access placement",
            "Plan for lifestyle changes"
        ],
        'Stage 5': [
            "Dialysis or transplant is necessary",
            "Strict adherence to medical regimen",
            "Monitor for complications",
            "Avoid activities that could cause bleeding",
            "Follow dialysis center instructions",
            "Maintain hope and stay positive",
            "Seek support from family and friends"
        ]
    }
    
    return tips_by_stage.get(ckd_stage, tips_by_stage['No CKD'])

# Complete Recommendation System
def generate_complete_recommendations(ckd_stage, age=None, gender=None, specific_concerns=None, language='en'):
    """
    Generate complete recommendations including diet, exercise, and AI suggestions
    """
    # Get basic diet and exercise plans
    diet_plan = get_diet_plan(ckd_stage, age, gender)
    exercise_plan = get_exercise_plan(ckd_stage, age, gender)
    
    # Get AI-powered personalized recommendations
    ai_recommendations = get_gemini_recommendations(ckd_stage, age, gender, specific_concerns, language)
    
    # Generate lifestyle tips based on stage
    lifestyle_tips = generate_lifestyle_tips(ckd_stage)
    
    return {
        'ckd_stage': ckd_stage,
        'diet_plan': diet_plan,
        'exercise_plan': exercise_plan,
        'lifestyle_tips': lifestyle_tips,
        'ai_recommendations': ai_recommendations,
        'generated_at': datetime.now().isoformat()
    }

# Test functions
def test_diet_plans():
    """Test diet plan generation for all stages"""
    test_stages = ['No CKD', 'Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5']
    for stage in test_stages:
        plan = get_diet_plan(stage)
        print(f"\n{stage} Diet Plan:")
        print(f"Breakfast: {plan['breakfast']}")
        print(f"Lunch: {plan['lunch']}")
        print(f"Dinner: {plan['dinner']}")
        print(f"Fluid Intake: {plan['fluid_intake']}")
        print(f"Sodium Limit: {plan['sodium_limit']}")

def test_exercise_plans():
    """Test exercise plan generation for all stages"""
    test_stages = ['No CKD', 'Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5']
    for stage in test_stages:
        plan = get_exercise_plan(stage)
        print(f"\n{stage} Exercise Plan:")
        print(f"Daily Activity: {plan['daily_activity']}")
        print(f"Recommended Exercises: {', '.join(plan['recommended_exercises'])}")
        print(f"Frequency: {plan['frequency']}")
        print(f"Intensity: {plan['intensity']}")
        print(f"Duration: {plan['duration']}")

def test_gemini_integration():
    """Test Gemini AI integration with sample cases"""
    test_cases = [
        {'stage': 'Stage 2', 'age': 45, 'gender': 'F', 'concerns': 'High blood pressure'},
        {'stage': 'Stage 3', 'age': 60, 'gender': 'M', 'concerns': 'Diabetes'},
        {'stage': 'No CKD', 'age': 35, 'gender': 'F', 'concerns': 'Prevention'}
    ]

    for case in test_cases:
        print(f"\n=== Personalized Recommendations for {case['stage']} Patient ===")
        recommendations = get_gemini_recommendations(
            case['stage'], 
            case['age'], 
            case['gender'], 
            case['concerns']
        )
        print(recommendations[:500] + "..." if len(recommendations) > 500 else recommendations)

def test_complete_system():
    """Test the complete recommendation system"""
    test_patient = {
        'stage': 'Stage 3',
        'age': 55,
        'gender': 'M',
        'concerns': 'High blood pressure and diabetes'
    }

    print("=== Complete Recommendation System Test ===")
    recommendations = generate_complete_recommendations(
        test_patient['stage'],
        test_patient['age'],
        test_patient['gender'],
        test_patient['concerns']
    )

    print(f"\nCKD Stage: {recommendations['ckd_stage']}")
    print(f"\nDiet Plan:")
    for key, value in recommendations['diet_plan'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print(f"\nExercise Plan:")
    for key, value in recommendations['exercise_plan'].items():
        if isinstance(value, list):
            print(f"  {key.replace('_', ' ').title()}: {', '.join(value)}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")

    print(f"\nLifestyle Tips:")
    for i, tip in enumerate(recommendations['lifestyle_tips'], 1):
        print(f"  {i}. {tip}")

    print(f"\nAI Recommendations (first 300 chars):")
    print(recommendations['ai_recommendations'][:300] + "...")

if __name__ == "__main__":
    print("=== Testing Recommendation Engine ===\n")
    
    # Test diet plans
    print("1. Testing Diet Plans:")
    test_diet_plans()
    
    # Test exercise plans
    print("\n2. Testing Exercise Plans:")
    test_exercise_plans()
    
    # Test Gemini integration
    print("\n3. Testing Gemini AI Integration:")
    test_gemini_integration()
    
    # Test complete system
    print("\n4. Testing Complete System:")
    test_complete_system()
    
    print("\n=== Recommendation Engine Test Complete ===")
