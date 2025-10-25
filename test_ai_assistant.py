#!/usr/bin/env python3
"""
Test script for AI Assistant functionality
"""

import requests
import json

def test_ai_assistant():
    """Test the AI assistant endpoint"""
    base_url = "http://127.0.0.1:5000"
    
    # Test data
    test_messages = [
        "Hello",
        "What is CKD?",
        "Tell me about diet for kidney disease",
        "Exercise recommendations",
        "ನಮಸ್ಕಾರ",
        "ಸಿಕೆಡಿ ಬಗ್ಗೆ ಹೇಳಿ"
    ]
    
    print("Testing AI Assistant...")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        print("-" * 30)
        
        try:
            # Test with English
            response = requests.post(
                f"{base_url}/api/chat",
                json={
                    "message": message,
                    "language": "en"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"SUCCESS Response: {data.get('response', 'No response')[:100]}...")
            else:
                print(f"ERROR: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"CONNECTION ERROR: {e}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("AI Assistant test completed!")

if __name__ == "__main__":
    test_ai_assistant()
