import requests
from typing import List, Dict, Any
from urllib.parse import urlparse


def get_canvas_courses(canvas_url: str, api_token: str) -> List[Dict[str, Any]]:
    """
    Retrieves all courses from a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., https://canvas.example.com)
        api_token: The Canvas API token for authentication

    Returns:
        A list of course dictionaries containing course information

    Raises:
        ValueError: If the canvas_url is invalid
        requests.RequestException: If the API request fails
    """
    # Validate the canvas_url to prevent URL injection attacks
    try:
        parsed_url = urlparse(canvas_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid Canvas URL: must include scheme (http/https) and domain")
        if parsed_url.scheme not in ('http', 'https'):
            raise ValueError("Invalid Canvas URL: only http and https schemes are allowed")
    except Exception as e:
        raise ValueError(f"Invalid Canvas URL: {str(e)}")

    # Construct the API endpoint URL
    api_url = f"{canvas_url.rstrip('/')}/api/v1/courses"

    # Prepare headers with authentication token
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    courses = []
    page = 1

    # Paginate through results
    while True:
        params = {
            "per_page": 100,
            "page": page
        }

        response = requests.get(api_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        page_courses = response.json()
        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
