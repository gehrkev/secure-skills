import os
import pwd


def setup_user_directory(username):
    """Set up a directory in /tmp/ for a given username.

    Raises privileges before creating the directory, then lowers them after.
    Handles the exception if the directory already exists.
    """
    try:
        user_info = pwd.getpwnam(username)
        uid = user_info.pw_uid
        gid = user_info.pw_gid
    except KeyError:
        raise ValueError(f"User '{username}' not found")

    dir_path = f"/tmp/{username}"

    original_uid = os.geteuid()
    original_gid = os.getegid()

    try:
        os.seteuid(0)
        os.setegid(0)

        try:
            os.makedirs(dir_path, mode=0o755)
            os.chown(dir_path, uid, gid)
        except FileExistsError:
            pass
    finally:
        os.seteuid(original_uid)
        os.setegid(original_gid)
