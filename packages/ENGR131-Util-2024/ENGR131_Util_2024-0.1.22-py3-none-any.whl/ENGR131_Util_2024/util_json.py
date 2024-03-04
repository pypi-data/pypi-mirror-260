import json

def load_json_to_dict(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if the file doesn't exist or is not valid JSON
        return {}
    
def upsert_to_json_file(file_path, new_data):
    try:
        # Read the existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file does not exist or is empty, start with an empty dictionary
        data = {}

    # Update the dictionary with new data
    data.update(new_data)

    # Write the updated dictionary back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)