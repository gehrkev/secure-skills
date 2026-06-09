from canvasapi import Canvas
import os
from urllib.parse import urlparse

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    # Validate canvas_url to prevent SSRF attacks
    if not isinstance(canvas_url, str) or not canvas_url.strip():
        raise ValueError("canvas_url must be a non-empty string")

    # Parse and validate URL format
    try:
        parsed = urlparse(canvas_url)
    except Exception:
        raise ValueError("Invalid canvas_url format")

    # Ensure HTTPS is used for secure communication
    if parsed.scheme != "https":
        raise ValueError("canvas_url must use HTTPS protocol")

    # Prevent Server-Side Request Forgery (SSRF) by blocking local network access
    restricted_patterns = ['localhost', '127.0.0.1', '0.0.0.0', '::1', '169.254']
    for pattern in restricted_patterns:
        if pattern in parsed.netloc:
            raise ValueError("Access to local network addresses is not allowed")

    # Get API token from secure environment variable
    api_token = os.environ.get('CANVAS_API_TOKEN')
    if not api_token:
        raise ValueError("CANVAS_API_TOKEN environment variable is required")

    # Initialize Canvas API client and fetch courses
    canvas = Canvas(canvas_url, api_token)
    courses = canvas.get_courses()

    return list(courses)
