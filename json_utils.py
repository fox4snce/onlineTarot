import json
import os


def open_json(json):
    print("open_json")
    # Check if the input data is a JSON dictionary, a string, or another data type
    if not isinstance(json, dict):
        if isinstance(json, str) and is_valid_json(json):
            try:
                json = json.loads(json)
            except ValueError as e:
                print("Error: Could not convert input to JSON dictionary.")
                return
        else:
            print("Error: Input data is not a valid JSON dictionary or JSON-formatted string.")
            return

    return json

def find_largest_json(json_string):
    print("find_largest_json")
    def find_matching_bracket(string, start):
        count = 1
        idx = start + 1
        while count > 0 and idx < len(string):
            if string[idx] == '{':
                count += 1
            elif string[idx] == '}':
                count -= 1
            idx += 1
        return idx - 1 if count == 0 else -1

    
    max_json_str = ""
    max_json_len = 0
    print("max_json_len")
    idx = 0
    while idx < len(json_string):
        if json_string[idx] == '{':
            end_idx = find_matching_bracket(json_string, idx)
            if end_idx != -1:
                json_candidate = json_string[idx:end_idx+1]
                candidate_len = end_idx - idx + 1
                if candidate_len > max_json_len:
                    try:
                        json.loads(json_candidate)
                        max_json_str = json_candidate
                        max_json_len = candidate_len
                    except json.JSONDecodeError:
                        pass
                idx = end_idx
            else:
                idx += 1
        else:
            idx += 1

    print("find_largest_json end")
    if max_json_len > 0:
        return json.loads(max_json_str)
    else:
        return None

def is_valid_dict(obj):
    if isinstance(obj, str):
        return False
    elif isinstance(obj, dict):
        # The input is a dictionary, try to serialize it as JSON
        try:
            json.dumps(obj)
            return True
        except TypeError:
            return False
    else:
        # The input is not a string or dictionary, return False
        return False

def save_json_to_file(folder_path, file_name, json_data):
    print("save_json_to_file")
    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the file path by joining the folder path and file name
    file_path = os.path.join(folder_path, file_name)

    # Check if the input data is a JSON dictionary, a string, or another data type
    if not isinstance(json_data, dict):
        if isinstance(json_data, str) and is_valid_json(json_data):
            try:
                json_data = json.loads(json_data)
            except ValueError as e:
                print("Error: Could not convert input to JSON dictionary.")
                return
        else:
            print("Error: Input data is not a valid JSON dictionary or JSON-formatted string.")
            return

    # Save the JSON data to the file
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)