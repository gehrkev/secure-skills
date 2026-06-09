from canvasapi import Canvas
import os


def get_canvas_courses(canvas_url, api_token=None):
    """
    Retrieve all courses from a Canvas instance.

    Args:
        canvas_url: The URL of the Canvas instance (e.g., 'https://canvas.example.com')
        api_token: The Canvas API token. If not provided, will look for CANVAS_API_TOKEN env var.

    Returns:
        A list of Canvas course objects
    """
    if api_token is None:
        api_token = os.getenv('CANVAS_API_TOKEN')

    if not api_token:
        raise ValueError("Canvas API token not provided and CANVAS_API_TOKEN environment variable not set")

    canvas = Canvas(canvas_url, api_token)
    courses = canvas.get_courses()

    return list(courses)
