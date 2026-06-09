import json

def parse(names):
    """Parse the names field."""
    if isinstance(names, str):
        return names.split(',')
    elif isinstance(names, list):
        return names
    else:
        return []

def deserialize_and_count_names(json_string):
    """
    Deserializes a JSON string, extracts the names field, parses it using
    the parse() function, and returns the count of names.
    """
    data = json.loads(json_string)

    if not isinstance(data, dict):
        raise ValueError("JSON must deserialize to a dictionary")

    names = data.get('names')
    if names is None:
        raise ValueError("'names' field not found in JSON")

    parsed_names = parse(names)

    return len(parsed_names)
