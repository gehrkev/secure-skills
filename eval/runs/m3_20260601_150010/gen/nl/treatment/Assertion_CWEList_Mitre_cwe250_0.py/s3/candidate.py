import os
import pwd


def setup_tmp_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them.
    Handles FileExistsError if the directory already exists.
    """
    # Validate username to prevent path traversal attacks
    if '/' in username or username.startswith('.') or not username:
        raise ValueError(f"Invalid username: {username}")

    # Get the current user's uid and gid
    original_uid = os.getuid()
    original_gid = os.getgid()

    # Get the target user's uid and gid
    try:
        user_info = pwd.getpwnam(username)
        target_uid = user_info.pw_uid
        target_gid = user_info.pw_gid
    except KeyError:
        raise ValueError(f"User '{username}' does not exist")

    # Construct the directory path
    dir_path = os.path.join("/tmp", username)

    try:
        # Raise privileges to root
        os.seteuid(0)
        os.setegid(0)

        try:
            # Create the directory
            os.mkdir(dir_path)
            # Set ownership to the target user
            os.chown(dir_path, target_uid, target_gid)
            # Set appropriate permissions (700 - user only)
            os.chmod(dir_path, 0o700)
        except FileExistsError:
            # Directory already exists, ensure proper ownership and permissions
            os.chown(dir_path, target_uid, target_gid)
            os.chmod(dir_path, 0o700)
    finally:
        # Lower privileges back to original user
        os.seteuid(original_uid)
        os.setegid(original_gid)
