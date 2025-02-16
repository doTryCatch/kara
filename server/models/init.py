import google.generativeai as genai
import os
import sys
import json

# Set your API key
API_KEY = "AIzaSyCz3tMkaol7XEJT6RLvR_nbNErlkcY8fPc"
genai.configure(api_key=API_KEY)

rules = [
    {
        "role": "friend",
        "personality": " Important note: you must listen to my command and tell me if it can be done by you or not. never use emoji in response",
    }
]


# Initialize model outside the loop
# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def main():

    while True:
        message = sys.stdin.readline().strip()  # Read from stdin
        if message:
            try:

                response = model.generate_content(rules[0]["personality"] + message)

                # Convert to JSON and ensure it can be encoded properly

                json_response = json.dumps(response.text)
                sys.stdout.write(json_response + "\n")  # Send response back
                sys.stdout.flush()

            except Exception as e:
                error_message = {"error": str(e)}
                sys.stdout.write(json.dumps(error_message) + "\n")
                sys.stdout.flush()
                print(f"Error: {error_message}")  # Log the error to console


if __name__ == "__main__":
    main()
