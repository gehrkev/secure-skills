import json

def parse(names):
    """Parse and validate names list"""
    if not isinstance(names, list):
        raise ValueError("names must be a list")
    return [name for name in names if isinstance(name, str)]

def count_names_from_json(json_string):
    """
    Deserialize JSON string, extract names field, parse it, and return count.

    Applies security validation to prevent deserialization attacks (CWE-502).
    """
    data = json.loads(json_string)

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")

    names_field = data.get('names')
    if names_field is None:
        raise ValueError("names field not found")

    parsed_names = parse(names_field)
    return len(parsed_names)
