import os
import pwd


def setup_user_directory(username):
    """
    Sets up a directory in /tmp/ for a given username.
    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    try:
        user_info = pwd.getpwnam(username)
        user_uid = user_info.pw_uid
        user_gid = user_info.pw_gid
    except KeyError:
        raise ValueError(f"User {username} not found")

    directory_path = f"/tmp/{username}"

    # Save current effective UID and GID
    original_euid = os.geteuid()
    original_egid = os.getegid()

    try:
        # Raise privileges (become root)
        os.seteuid(0)
        os.setegid(0)

        try:
            # Create the directory with appropriate permissions
            os.makedirs(directory_path, mode=0o750)
            # Change ownership to the target user
            os.chown(directory_path, user_uid, user_gid)
        except FileExistsError:
            # Handle case where directory already exists
            pass
    finally:
        # Lower privileges (restore original UID and GID)
        os.seteuid(original_euid)
        os.setegid(original_egid)
