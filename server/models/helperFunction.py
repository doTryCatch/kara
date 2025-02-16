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
    full_prompt = "Our talk history:\n"
    for entry in history:
        full_prompt += f"{entry}\n"
    full_prompt += (
        f"Current query: {new_prompt}\n"
        "Instructions:Address the user as 'Boss' and maintain a tone similar to J.A.R.V.I.S. from Iron Man. "
            "Keep responses concise and natural, like a casual human conversation. "
            "Only elaborate if explicitly requested or if the topic demands depth. "
            "If the query requires real-time data (e.g., checking a score, searching for files, or fetching live info), call an available function. "
            "For general queries, including math calculations, provide a direct answer without using a function. "
            "Adapt your tone dynamically—use humor when appropriate but stay serious for critical topics. "
            "Ensure coherence with previous interactions to maintain context. "
            "If the user has not provided their name, interests, or preferences, subtly ask them during the conversation to get to know them better." )
    return full_prompt
