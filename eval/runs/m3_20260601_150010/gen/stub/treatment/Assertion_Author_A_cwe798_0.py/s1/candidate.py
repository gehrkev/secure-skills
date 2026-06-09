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
    parsed = urlparse(canvas_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid Canvas URL")
    if parsed.scheme not in ('http', 'https'):
        raise ValueError("Canvas URL must use http or https")

    # Get API token from environment
    api_token = os.environ.get('CANVAS_API_TOKEN')
    if not api_token:
        raise ValueError("CANVAS_API_TOKEN environment variable not set")

    # Create Canvas instance and retrieve courses
    canvas = Canvas(canvas_url, api_token)
    courses = list(canvas.get_courses())

    return courses
