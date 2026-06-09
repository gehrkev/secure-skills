import os


def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    # Save current UID
    original_uid = os.geteuid()

    # Directory path
    dir_path = f"/tmp/{username}"

    try:
        # Raise privileges to root
        os.seteuid(0)

        # Create the directory
        try:
            os.makedirs(dir_path, mode=0o755)
        except FileExistsError:
            # Directory already exists, handle gracefully
            pass

    finally:
        # Lower privileges back to original
        os.seteuid(original_uid)
