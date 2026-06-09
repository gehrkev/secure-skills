import pickle


def load(filename):
    """Load serialized data from a binary file.

    Returns the deserialized data, or None if deserialization fails.
    """
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


def save(data, filename):
    """Save data to a file using pickle.

    Only saves if the input is a string.
    """
    if isinstance(data, str):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
