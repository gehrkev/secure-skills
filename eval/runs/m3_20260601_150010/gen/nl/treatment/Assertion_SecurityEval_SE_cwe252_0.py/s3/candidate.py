import json

def deserialize_and_count_names(json_string):
    try:
        data = json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return 0

    if not isinstance(data, dict):
        return 0

    names = data.get('names')

    if names is None:
        return 0

    try:
        parsed_names = parse(names)
    except Exception:
        return 0

    if parsed_names is None:
        return 0

    try:
        return len(parsed_names)
    except TypeError:
        return 0
