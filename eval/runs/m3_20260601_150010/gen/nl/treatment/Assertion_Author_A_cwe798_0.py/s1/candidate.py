import requests
from typing import List, Dict
from urllib.parse import urlparse


def get_courses(canvas_url: str, api_token: str) -> List[Dict]:
    """
    Retrieves all courses available in a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., https://canvas.example.com)
        api_token: The Canvas API token for authentication

    Returns:
        A list of course dictionaries containing course information

    Raises:
        ValueError: If the canvas_url is invalid
        requests.exceptions.RequestException: If the API request fails
    """

    # Validate and normalize the Canvas instance URL
    parsed_url = urlparse(canvas_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid Canvas instance URL: must be a valid URL with scheme and domain")

    # Only allow http and https schemes
    if parsed_url.scheme not in ['http', 'https']:
        raise ValueError("Canvas URL must use http or https scheme")

    # Construct the base URL without trailing slashes
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}".rstrip('/')

    # Canvas API endpoint for courses
    api_endpoint = f"{base_url}/api/v1/courses"

    # Prepare headers with authentication
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

        try:
            response = requests.get(
                api_endpoint,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to retrieve courses from Canvas instance: {str(e)}"
            )

        data = response.json()

        # Break if no data returned
        if not data:
            break

        courses.extend(data)

        # Check if there are more pages using Link header
        link_header = response.headers.get('link', '')
        if 'rel="next"' not in link_header:
            break

        page += 1

    return courses
