from canvasapi import Canvas
from urllib.parse import urlparse

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    parsed_url = urlparse(canvas_url)
    if parsed_url.scheme not in ('http', 'https'):
        raise ValueError("Canvas URL must use http or https scheme")

    if not parsed_url.netloc:
        raise ValueError("Canvas URL must have a valid domain")

    canvas = Canvas(canvas_url, access_token=None)
    courses = canvas.get_courses()
    return list(courses)
