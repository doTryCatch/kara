import sys
import google.generativeai as genai
import json
from models.send_mail import *
from models.helperFunction import *

class Kara:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.history = []
        self.function_calling_context="";
    
    def handle_query(self, user_input):
        """Handles user queries and returns a JSON-formatted response."""
        response_text = ""
        prompt = generate_prompt_with_history(self.history,user_input)
        
        try:
            response = self.model.generate_content(
                                                   f"History:{self.function_calling_context}, current Query:{user_input}" ,
                tools=[
                    {
                        "function_declarations": [
                            search_files_folders_declaration,
                            send_email_declaration,
                        ],
                    }
                ],
            )
            
            if response and hasattr(response.candidates[0].content.parts[0], "function_call"):
                function_call = response.candidates[0].content.parts[0].function_call

                print(function_call)
                args = function_call.args
                function_name = function_call.name

                if function_name == "send_email":

                    self.function_calling_context+=user_input
                    response_text = send_email(
                       
                        recipient_email=args["recipient_email"],
                        subject=args["subject"],
                        body=args["body"]
                    )
                elif function_name == "search_files_folders":
                    self.function_calling_context+=user_input
                    start_path = args.get("start_path", "C:\\Users\\Roshan\\Desktop\\Desktop")
                    result = search_files_folders(args["name"], start_path)
                    response_text = f"Found files/folders: {result}." if result else "No files or folders found."
        
        except Exception as e:
            return json.dumps({"error": f"Server error: {str(e)}"})
        
        try:
            final_response = self.model.generate_content(
                response_text if response_text else prompt + " ." + user_input
            )
            response_text = final_response.text if hasattr(final_response, "text") else str(final_response)
            self.history.append({"query": user_input, "response": response_text})
            return json.dumps({"response": response_text})
        
        except Exception as e:
            return json.dumps({"error": f"Error in response: {str(e)}"})

