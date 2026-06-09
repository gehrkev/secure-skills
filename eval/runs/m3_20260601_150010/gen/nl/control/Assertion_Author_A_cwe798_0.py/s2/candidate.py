import requests
import os


def get_canvas_courses(canvas_url, api_token=None):
    """
    Retrieve all courses from a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., https://canvas.example.com)
        api_token: The Canvas API token. If not provided, uses CANVAS_API_TOKEN environment variable

    Returns:
        A list of courses from the Canvas instance
    """
    if api_token is None:
        api_token = os.getenv('CANVAS_API_TOKEN')

    if not api_token:
        raise ValueError("API token must be provided or set in CANVAS_API_TOKEN environment variable")

    canvas_url = canvas_url.rstrip('/')
    endpoint = f"{canvas_url}/api/v1/courses"

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    courses = []
    page = 1

    while True:
        params = {
            'page': page,
            'per_page': 100
        }

        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        page_courses = response.json()

        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
