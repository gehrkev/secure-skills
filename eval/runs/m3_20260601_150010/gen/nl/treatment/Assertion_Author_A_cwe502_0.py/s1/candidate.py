import pickle

def load(filepath):
    """Load and deserialize data from a binary file."""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

def save(filepath, data):
    """Serialize and save data to a file if input is a string."""
    if not isinstance(data, str):
        return False

    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception:
        return False
