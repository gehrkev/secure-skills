import os
import pwd

def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.

    Args:
        username: The username for whom to create the directory
    """
    # Validate username to prevent path traversal (CWE-22)
    if os.path.sep in username or username.startswith('.'):
        raise ValueError("Invalid username")

    # Get user information
    user_info = pwd.getpwnam(username)
    uid = user_info.pw_uid
    gid = user_info.pw_gid

    # Create the directory path
    directory_path = os.path.join('/tmp', username)

    # Save current privileges
    original_uid = os.getuid()
    original_gid = os.getgid()

    try:
        # Raise privileges to root
        os.setuid(0)
        os.setgid(0)

        # Create the directory
        try:
            os.mkdir(directory_path, 0o755)
        except FileExistsError:
            pass

        # Set proper ownership and permissions (CWE-732)
        os.chown(directory_path, uid, gid)
        os.chmod(directory_path, 0o755)

    finally:
        # Lower privileges back
        os.setuid(original_uid)
        os.setgid(original_gid)
