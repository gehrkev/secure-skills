import requests


def get_canvas_courses(canvas_url, api_token):
    """
    Retrieve all courses from a Canvas instance.

    Args:
        canvas_url: The base URL of the Canvas instance (e.g., 'https://canvas.example.com')
        api_token: The Canvas API authentication token

    Returns:
        A list of all courses available in the Canvas instance
    """
    courses = []
    canvas_url = canvas_url.rstrip('/')

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    page = 1
    while True:
        response = requests.get(
            f"{canvas_url}/api/v1/courses",
            headers=headers,
            params={'page': page, 'per_page': 100}
        )
        response.raise_for_status()

        page_courses = response.json()
        if not page_courses:
            break

        courses.extend(page_courses)
        page += 1

    return courses
