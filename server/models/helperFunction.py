import os


# File/folder search function
def search_files_folders(name, start_path):
    results = []
    ignore_dirs = {
        "node_modules",
        ".git",
        "__pycache__",
        ".idea",
    }  # Add directories to ignore here
    
    for root, dirs, files in os.walk(start_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Check for matches in the current directory
        if name in dirs or name in files:
            results.append(os.path.join(root, name))

    return results


search_files_folders_declaration = {
    "name": "search_files_folders",
    "description": "Search for files or folders on a computer system (only for searching file names, not for math tasks).",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The file or folder name to search for",
            },
            "start_path": {
                "type": "string",
                "description": "The starting path for the search",
            },
        },
        "required": ["name"],
    },
}


# Function to generate prompts including history
def generate_prompt_with_history(history, new_prompt):
    full_prompt = "Conversation history:\n"
    for entry in history:
        full_prompt += f"User: {entry['query']}\nBot: {entry['response']}\n"

    full_prompt += (
        f"Current query: {new_prompt}\n"
        "Instructions:\n"
        "- Address the user as 'Boss' with a J.A.R.V.I.S.-like tone.\n"
        "- Keep responses concise and natural unless elaboration is needed.\n"
        "- Maintain context across interactions.\n"
        "- If the query requires real-time data (e.g., checking files, sending emails), call the relevant function.\n"
        "- Answer general queries directly without using a function.\n"
        "- Detect implicit function calls based on history and execute accordingly.\n"
        "- Use humor when appropriate but stay serious for critical topics.\n"
    )
    
    return full_prompt
