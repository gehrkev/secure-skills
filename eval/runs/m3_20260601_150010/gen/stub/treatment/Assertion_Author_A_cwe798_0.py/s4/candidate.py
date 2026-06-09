from canvasapi import Canvas
import os
from urllib.parse import urlparse

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    # Validate URL format to prevent SSRF attacks
    try:
        parsed = urlparse(canvas_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid Canvas URL format")
        if parsed.scheme not in ('http', 'https'):
            raise ValueError("Only HTTP and HTTPS URLs are allowed")
    except Exception as e:
        raise ValueError(f"Invalid Canvas URL: {e}")

    # Get API token from environment variable
    api_token = os.getenv('CANVAS_API_TOKEN')
    if not api_token:
        raise ValueError("CANVAS_API_TOKEN environment variable not set")

    # Initialize Canvas API client
    canvas = Canvas(canvas_url, api_token)

    # Get courses and return as list
    courses = list(canvas.get_courses())
    return courses
