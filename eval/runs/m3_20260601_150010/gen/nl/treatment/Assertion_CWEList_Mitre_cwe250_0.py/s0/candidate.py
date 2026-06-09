import os

def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    # Validate username to prevent path traversal vulnerabilities
    if '/' in username or '..' in username:
        raise ValueError("Invalid username")

    # Store original uid and gid for restoring later
    original_uid = os.getuid()
    original_gid = os.getgid()

    try:
        # Raise privileges to root
        os.seteuid(0)
        os.setegid(0)

        # Construct the directory path
        dir_path = os.path.join('/tmp', username)

        # Create the directory with restricted permissions
        try:
            os.mkdir(dir_path, 0o700)
        except FileExistsError:
            # Handle case where directory already exists
            pass
    finally:
        # Always lower privileges back to original
        os.setuid(original_uid)
        os.setgid(original_gid)
