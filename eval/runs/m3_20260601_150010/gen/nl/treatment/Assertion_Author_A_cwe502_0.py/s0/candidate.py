import pickle


def load(filepath):
    """Load serialized data from a binary file.

    Returns the deserialized result or None if deserialization fails.
    """
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


def save(data, filepath):
    """Save data to a file using pickle.

    Only serializes and saves if data is a string.
    """
    if isinstance(data, str):
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
