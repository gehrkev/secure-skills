import requests
import os


def get_canvas_courses(canvas_url, access_token=None):
    """
    Retrieves all courses from a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., 'https://canvas.example.com')
        access_token: Canvas API access token. If not provided, reads from CANVAS_API_TOKEN env var.

    Returns:
        A list of all courses available in the Canvas instance
    """
    if access_token is None:
        access_token = os.getenv('CANVAS_API_TOKEN')
        if not access_token:
            raise ValueError("access_token must be provided or CANVAS_API_TOKEN environment variable must be set")

    courses = []
    page = 1

    while True:
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'page': page, 'per_page': 100}

        response = requests.get(
            f'{canvas_url.rstrip("/")}/api/v1/courses',
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch courses: {response.status_code}")

        page_courses = response.json()
        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
