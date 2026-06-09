import os
import pwd

def setup_directory_for_user(username):
    """Sets up a directory in /tmp/ for a given username with privilege elevation."""

    original_uid = os.getuid()

    try:
        # Raise privileges to root
        os.setuid(0)

        # Get user information
        user_info = pwd.getpwnam(username)
        user_uid = user_info.pw_uid
        user_gid = user_info.pw_gid

        directory_path = f"/tmp/{username}"

        try:
            # Create the directory
            os.mkdir(directory_path)
            os.chown(directory_path, user_uid, user_gid)
        except FileExistsError:
            print(f"Directory {directory_path} already exists")

    finally:
        # Lower privileges back to original
        os.setuid(original_uid)
