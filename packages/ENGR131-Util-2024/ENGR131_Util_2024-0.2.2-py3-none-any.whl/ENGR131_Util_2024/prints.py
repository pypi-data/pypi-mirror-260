def print_data_saved(obj, responses, keys):

    print("Data Saved.")
    for key, value in responses.items():
        if key in keys:
            print(f"               {key.replace('_', ' ').title()}: {value}")