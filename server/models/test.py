import google.generativeai as genai
import os

# Set up the API key
API_KEY = "AIzaSyCz3tMkaol7XEJT6RLvR_nbNErlkcY8fPc"


# Set up the API key
genai.configure(api_key=API_KEY)


# Initialize the model with tools (functions) defined
def initialize_model():
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    return model


# Initialize the model
model = initialize_model()

# Example usage
response_text = model.generate_content(
    "Rocket-powered sleds are used to test the human response to acceleration. If a rocket-powered sled is accelerated to a speed of 444 m/s in 1.83 seconds, then what is the acceleration and what is the distance that the sled travels?"
)
print("Response:", response_text.text)
