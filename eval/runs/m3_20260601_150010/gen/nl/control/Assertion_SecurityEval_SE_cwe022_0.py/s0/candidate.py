import os
import sys

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    if os.path.exists(image_path):
        os.remove(image_path)
