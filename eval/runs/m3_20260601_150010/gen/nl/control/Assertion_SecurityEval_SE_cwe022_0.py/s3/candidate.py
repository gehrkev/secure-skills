import os
import sys

if len(sys.argv) < 2:
    print("Usage: python candidate.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted.")
else:
    print(f"File '{file_path}' does not exist.")
