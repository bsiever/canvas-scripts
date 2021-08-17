#!/usr/local/bin/python3
# TODO: Update above if needed
import sys
from canvasapi import Canvas
from string import Template

from CanvasSettings import *

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

emails = set()
noEmail = set()

# Could also include TAs if needed
for u in course.get_users(enrollment_type=["student", "observer", "student_view"]):
    if hasattr(u, 'email'):
        emails.add(u.email)
    else:
        noEmail.add(u)
        
print("-----Email-----")
for e in emails:
    print(e)

