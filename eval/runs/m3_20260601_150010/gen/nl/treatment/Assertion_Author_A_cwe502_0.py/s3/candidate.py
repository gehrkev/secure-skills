import pickle

def load(filename):
    """Load serialized data from a binary file and return the result, or None if deserialization fails."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

def save(data, filename):
    """Serialize data to a file, but only if the input is a string."""
    if isinstance(data, str):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
