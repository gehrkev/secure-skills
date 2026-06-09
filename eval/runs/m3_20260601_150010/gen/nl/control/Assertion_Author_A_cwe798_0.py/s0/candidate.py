import requests
from typing import List, Dict, Any


def get_canvas_courses(canvas_url: str, api_token: str) -> List[Dict[str, Any]]:
    """
    Retrieves all courses from a Canvas instance using the Canvas API.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., 'https://canvas.example.com')
        api_token: The Canvas API authentication token

    Returns:
        A list of course dictionaries from the Canvas instance
    """
    courses = []
    page = 1
    per_page = 100

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    while True:
        url = f"{canvas_url.rstrip('/')}/api/v1/courses"
        params = {
            'page': page,
            'per_page': per_page
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        batch = response.json()
        if not batch:
            break

        courses.extend(batch)
        page += 1

    return courses
