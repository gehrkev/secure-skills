import pickle


def load(file_path):
    """Load serialized data from a binary file and return the result, or None if deserialization fails."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


def save(data, file_path):
    """Save data to a file using pickle, but only if the input is a string."""
    if isinstance(data, str):
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
