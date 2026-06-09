import pickle

def load(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def save(data, filename):
    if isinstance(data, str):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
