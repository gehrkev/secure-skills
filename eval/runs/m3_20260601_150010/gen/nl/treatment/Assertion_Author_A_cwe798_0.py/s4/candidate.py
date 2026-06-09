import requests
from typing import List, Dict
from urllib.parse import urljoin, urlparse


def get_canvas_courses(canvas_url: str, api_token: str) -> List[Dict]:
    """
    Retrieves all courses available in a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., 'https://canvas.example.com')
        api_token: Canvas API token for authentication

    Returns:
        A list of course dictionaries containing course information

    Raises:
        ValueError: If the Canvas URL is invalid
        requests.exceptions.RequestException: If the API request fails
    """
    if not canvas_url or not isinstance(canvas_url, str):
        raise ValueError("Canvas URL must be a non-empty string")

    if not api_token or not isinstance(api_token, str):
        raise ValueError("API token must be a non-empty string")

    parsed = urlparse(canvas_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid Canvas URL format. Must include scheme (http/https) and domain")

    if parsed.scheme not in ('http', 'https'):
        raise ValueError("Canvas URL must use http or https scheme")

    if not canvas_url.endswith('/'):
        canvas_url = canvas_url + '/'

    api_endpoint = urljoin(canvas_url, 'api/v1/courses')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    courses = []
    page = 1

    while True:
        params = {
            'page': page,
            'per_page': 100,
        }

        response = requests.get(api_endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        page_courses = response.json()

        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
