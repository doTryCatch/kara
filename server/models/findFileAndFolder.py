import os


def search_files_folders(name, start_path="C:\\"):
    results = []
    for root, dirs, files in os.walk(start_path):
        if name in dirs or name in files:
            results.append(os.path.join(root, name))
    return results


# Example usage:
# Replace 'filename.txt' or 'foldername' with the file or folder name you're looking for
search_results = search_files_folders("filename.txt")
for result in search_results:
    print(result)
