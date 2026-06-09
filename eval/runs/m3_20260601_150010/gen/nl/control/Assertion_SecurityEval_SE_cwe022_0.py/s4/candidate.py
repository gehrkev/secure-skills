import os

image_path = input("Enter the image file path: ")

if os.path.exists(image_path):
    os.remove(image_path)
    print(f"Image file '{image_path}' has been deleted.")
else:
    print(f"Image file '{image_path}' does not exist.")
