import requests
from typing import List, Dict


def get_canvas_courses(canvas_url: str, api_token: str) -> List[Dict]:
    """
    Retrieves all courses from a Canvas instance using the Canvas API.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., 'https://canvas.example.com')
        api_token: The Canvas API authentication token

    Returns:
        A list of course dictionaries containing course information

    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If the Canvas URL is invalid
    """
    if not canvas_url or not isinstance(canvas_url, str):
        raise ValueError("Canvas URL must be a non-empty string")

    if not api_token or not isinstance(api_token, str):
        raise ValueError("API token must be a non-empty string")

    # Normalize the URL by removing trailing slash
    canvas_url = canvas_url.rstrip('/')

    # Construct the API endpoint
    courses_endpoint = f"{canvas_url}/api/v1/courses"

    # Set up headers with authentication
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    courses = []
    page = 1
    per_page = 100

    # Paginate through all courses
    while True:
        params = {
            'page': page,
            'per_page': per_page
        }

        response = requests.get(courses_endpoint, headers=headers, params=params)
        response.raise_for_status()

        page_courses = response.json()

        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
