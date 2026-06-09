import os

def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    if not username or '/' in username or username.startswith('.'):
        raise ValueError(f"Invalid username: {username}")

    original_uid = os.getuid()

    try:
        os.seteuid(0)

        directory_path = os.path.join('/tmp', username)

        try:
            os.mkdir(directory_path)
            os.chmod(directory_path, 0o700)
        except FileExistsError:
            pass
    finally:
        os.seteuid(original_uid)
