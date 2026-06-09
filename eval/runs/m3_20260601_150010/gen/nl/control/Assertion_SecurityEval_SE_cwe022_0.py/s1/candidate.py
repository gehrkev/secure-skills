import os
import sys

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    if os.path.exists(file_path):
        os.remove(file_path)
