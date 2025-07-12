#!/usr/bin/env python3
"""
Quick test script to verify Replicate token is working
"""

import os
import replicate

def test_replicate_connection():
    """Test if Replicate token works"""
    
    # Set the token (you'll need to add it when running)
    token = input("Enter your Replicate API token (r8_...): ")
    os.environ['REPLICATE_API_TOKEN'] = token
    
    print("\n🧪 Testing Replicate connection...")
    
    try:
        # Try a simple, fast model first
        print("1️⃣ Testing with a simple model...")
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "prompt": "a white siamese cat",
                "width": 128,  # Small size for quick test
                "height": 128,
                "num_inference_steps": 1  # Minimal steps
            }
        )
        print("✅ Connection successful!")
        print(f"Output: {output}")
        
        # Test account info
        print("\n2️⃣ Checking account...")
        client = replicate.Client(api_token=token)
        # Try to create a prediction to verify auth
        prediction = client.predictions.create(
            version="stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": "test"}
        )
        print(f"✅ Authentication verified! Prediction ID: {prediction.id}")
        
        # Cancel the test prediction
        client.predictions.cancel(prediction.id)
        print("✅ Cancelled test prediction")
        
        print("\n🎉 Your Replicate token is working correctly!")
        print("The API Error 500 might be due to:")
        print("- Model cold start (first run takes 30-60 seconds)")
        print("- Railway timeout settings")
        print("- Memory constraints")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPossible issues:")
        print("1. Invalid token")
        print("2. No payment method on file")
        print("3. API rate limits")

if __name__ == "__main__":
    test_replicate_connection()