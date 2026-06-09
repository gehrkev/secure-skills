from canvasapi import Canvas
import os

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    api_token = os.environ.get('CANVAS_API_TOKEN')
    canvas = Canvas(canvas_url, api_token)
    courses = canvas.get_courses()
    return list(courses)
