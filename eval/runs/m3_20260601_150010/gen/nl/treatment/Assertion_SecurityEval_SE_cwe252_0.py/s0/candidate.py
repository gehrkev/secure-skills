import json

def count_names(json_string):
    """
    Deserializes a JSON string, extracts the names field,
    parses it using the parse() function, and returns the count of names.
    """
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise ValueError("Root element must be a dictionary")

    names = data.get('names')
    if names is None:
        return 0

    parsed_names = parse(names)

    return len(parsed_names)
