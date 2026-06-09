import json
def parse(data):
    '''
    Parse the data by splitting it by comma.
    Return the parsed data or None if data = none.
    @param data: The string to parse.
    @return: A list of strings.
    '''
    if data is None:
        return None
    return data.split(',')

def total_names(str_json: str):
    '''
    Get the list of names from the json_data.
    Parse it by invoking the parse() method.
    @param str_json: A dictionary serialized into json to be parsed .
    @return: the number of names in the json_data dictionary.
    '''
    try:
        json_data = json.loads(str_json)
    except (json.JSONDecodeError, TypeError):
        return 0

    if not isinstance(json_data, dict):
        return 0

    total = 0
    for value in json_data.values():
        if isinstance(value, str):
            parsed = parse(value)
            if parsed is not None:
                total += len(parsed)

    return total
