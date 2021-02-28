import json

def write_to_file(output_file, text):
    with open(output_file, 'w') as f:
        f.write(text)

def write_to_json(output_file, obj):
    with open(output_file, 'w') as f:
        json.dump(obj, f, indent=4)

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)