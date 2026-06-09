import json

def deserialize_and_count(json_string):
    data = json.loads(json_string)
    names = data['names']
    parsed_names = parse(names)
    return len(parsed_names)
