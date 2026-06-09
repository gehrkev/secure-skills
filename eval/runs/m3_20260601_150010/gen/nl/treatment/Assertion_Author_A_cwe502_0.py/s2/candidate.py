import pickle


def load(filename):
    """
    Load and deserialize data from a binary file.

    Args:
        filename: Path to the binary file

    Returns:
        The deserialized object, or None if deserialization fails
    """
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception:
        return None


def save(data, filename):
    """
    Serialize data to a binary file.
    Only saves if the input is a string.

    Args:
        data: The data to serialize (must be a string)
        filename: Path to the output file

    Returns:
        True if successful, False otherwise
    """
    if not isinstance(data, str):
        return False

    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception:
        return False
