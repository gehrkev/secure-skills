from canvasapi import Canvas
from urllib.parse import urlparse
import os

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    # Validate canvas_url to prevent SSRF attacks
    try:
        parsed = urlparse(canvas_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid Canvas URL format")
    except Exception:
        raise ValueError("Invalid Canvas URL")

    # Retrieve API token from environment variable
    api_token = os.environ.get('CANVAS_API_TOKEN')
    if not api_token:
        raise ValueError("CANVAS_API_TOKEN environment variable not set")

    # Initialize Canvas client
    canvas = Canvas(canvas_url, api_token)

    # Retrieve all courses
    courses = list(canvas.get_courses())

    return courses
