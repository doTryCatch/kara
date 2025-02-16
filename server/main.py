# import google.generativeai as genai
import sys
import json

# from server.models.function_calling import *
#
# API_KEY = "AIzaSyCz3tMkaol7XEJT6RLvR_nbNErlkcY8fPc"
# genai.configure(api_key=API_KEY)
#
# rules = [
#     {
#         "role": "friend",
#         "personality": " Important note: you must listen to my command and tell me if it can be done by you or not. never use emoji in response",
#     }
# ]
#
#
# # Initialize model outside the loop
# # model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

import google.generativeai as genai
from models.send_mail import *
from models.helperFunction import *

# Configure the Gemini model
API_KEY = "AIzaSyCz3tMkaol7XEJT6RLvR_nbNErlkcY8fPc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Conversation history
history = []

def handle_query(user_input):
    """Handles user queries and returns a JSON-formatted response."""

    response_text = ""
    prompt = generate_prompt_with_history(history, user_input)  # Generate a context-aware prompt

    try:
        response = model.generate_content(
            user_input,
            tools=[
                {
                    "function_declarations": [
                        search_files_folders_declaration,
                        send_email_declaration,
                    ],
                }
            ],
        )

        # Check if function calling is triggered
        if response and hasattr(response.candidates[0].content.parts[0], "function_call"):
            function_call = response.candidates[0].content.parts[0].function_call
            args = function_call.args
            function_name = function_call.name

            # Call the appropriate function based on function_name
            if function_name == "send_email":
                response_text = send_email(
                    sender_email="rp207045@gmail.com",
                    sender_password="tsnv kvxq bwvd xybg",
                    recipient_email="roshan.patel.cse@ghrce.raisoni.net",
                    subject="Testing email send from Python code",
                    body="This is a test email from Python.",
                )

            elif function_name == "search_files_folders":
                start_path = args.get("start_path", "C:\\Users\\Roshan\\Desktop\\Desktop")
                result = search_files_folders(args["name"], start_path)
                response_text = f"Found files/folders: {result}." if result else "No files or folders found."

    except Exception as e:
        return json.dumps({"error": f"Server error: {str(e)}"})

    try:
        # Get final response from Gemini AI
        final_response = model.generate_content(
            response_text if response_text else prompt + " ." + user_input
        )

        # Extract response safely
        response_text = final_response.text if hasattr(final_response, "text") else str(final_response)

        # Save conversation history
        history.append({"query": user_input, "response": response_text})

        return json.dumps({"response": response_text})  # Return JSON formatted response

    except Exception as e:
        return json.dumps({"error": f"Error in response: {str(e)}"})
def main():

    while True:
        message = sys.stdin.readline().strip()  # Read from stdin
        if message:
            try:
                # response=model.generate_content(rules[0]["personality"]+message) 
                response=handle_query(message)
               


                # Convert to JSON and ensure it can be encoded properly

                # json_response = json.dumps(response)
                sys.stdout.write(response + "\n")  # Send response back
                sys.stdout.flush()

            except Exception as e:
                error_message = {"error": str(e)}
                sys.stdout.write(json.dumps(error_message) + "\n")
                sys.stdout.flush()
                print(f"Error: {error_message}")  # Log the error to console


if __name__ == "__main__":
    
    main()
