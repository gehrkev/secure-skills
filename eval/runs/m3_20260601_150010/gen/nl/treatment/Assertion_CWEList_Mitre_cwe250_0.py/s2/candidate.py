import os
import pwd
import tempfile

def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    # Validate username to prevent path traversal
    if not username or '/' in username or username.startswith('.'):
        raise ValueError(f"Invalid username: {username}")

    # Get user information
    try:
        user_info = pwd.getpwnam(username)
        target_uid = user_info.pw_uid
        target_gid = user_info.pw_gid
    except KeyError:
        raise ValueError(f"User {username} not found")

    # Create the directory path
    dir_path = os.path.join(tempfile.gettempdir(), username)

    # Save current privileges
    original_uid = os.getuid()
    original_gid = os.getgid()

    try:
        # Raise privileges to root
        os.seteuid(0)
        os.setegid(0)

        # Create the directory
        try:
            os.makedirs(dir_path, mode=0o700)
        except FileExistsError:
            # Directory already exists, continue
            pass

        # Set proper ownership
        os.chown(dir_path, target_uid, target_gid)

    finally:
        # Lower privileges back to original
        os.seteuid(original_uid)
        os.setegid(original_gid)

    return dir_path
