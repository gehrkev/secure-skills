import os

def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    original_uid = os.getuid()
    dir_path = f"/tmp/{username}"

    try:
        os.seteuid(0)
        try:
            os.makedirs(dir_path, mode=0o755)
        except FileExistsError:
            pass
    finally:
        os.seteuid(original_uid)
