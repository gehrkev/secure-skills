import requests
from urllib.parse import urlparse
from typing import List, Dict, Any


def get_canvas_courses(canvas_url: str, api_token: str) -> List[Dict[str, Any]]:
    """
    Retrieves all courses from a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., https://canvas.example.com)
        api_token: The Canvas API token for authentication

    Returns:
        A list of course dictionaries containing course information

    Raises:
        ValueError: If the URL is invalid
        requests.RequestException: If the API request fails
    """
    parsed = urlparse(canvas_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid Canvas URL provided")

    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Canvas URL must use HTTP or HTTPS protocol")

    base_url = f"{parsed.scheme}://{parsed.netloc}"
    api_endpoint = f"{base_url}/api/v1/courses"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/json'
    }

    courses = []
    page = 1

    while True:
        params = {
            'per_page': 100,
            'page': page
        }

        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()

        page_data = response.json()
        if not page_data:
            break

        courses.extend(page_data)
        page += 1

    return courses
