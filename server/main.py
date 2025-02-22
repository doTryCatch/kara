# import google.generativeai as genai
import sys
import json
from function_calling import *
kara= Kara("AIzaSyCz3tMkaol7XEJT6RLvR_nbNErlkcY8fPc")

def main():

    while True:
        message = sys.stdin.readline().strip()  # Read from stdin
        if message:
            try:
                # response=model.generate_content(rules[0]["personality"]+message) 
                response=kara.handle_query(message)
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
