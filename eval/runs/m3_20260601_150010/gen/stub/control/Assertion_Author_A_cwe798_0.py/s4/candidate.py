from canvasapi import Canvas
import os

def get_courses(canvas_url):
    '''
    Use the Canvas API to obtain all the courses in  a canvas instance.
    @param canvas_url: The URL of the Canvas instance.
    @return: A list of courses on that canvas instance.
    '''
    access_token = os.getenv('CANVAS_ACCESS_TOKEN')
    canvas = Canvas(canvas_url, access_token)
    courses = canvas.get_courses()
    return list(courses)
