import json

def count_names(json_string):
    """Deserializes JSON, extracts names field, parses it, and returns the count."""
    data = json.loads(json_string)

    if not isinstance(data, dict):
        raise TypeError("JSON must deserialize to a dictionary")

    if 'names' not in data:
        raise KeyError("Missing 'names' field")

    parsed_names = parse(data['names'])
    return len(parsed_names)
