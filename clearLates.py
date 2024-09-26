#!/usr/local/bin/python3

from canvasapi import Canvas
from CanvasSettings import *
from canvasUpdates import *
from sys import argv

# Expect one command line argument with the Canvas assignment ID
if len(argv) != 2:
    print("Usage: clearLates.py <assignmentID>")
    exit(1)

# Get the assignment ID from the command line
canvasIdForAssignment = argv[1]


# Initialize a new Canvas object
print("Connecting to Canvas...")
canvas = Canvas(API_URL, API_KEY)
print("Getting course...")
course = canvas.get_course(COURSE_ID)

# Also read in the Canvas data for the part
print(f"Getting canvas assignment: {canvasIdForAssignment}")
assignmentObject = course.get_assignment(canvasIdForAssignment)
print(assignmentObject.name)


users = [s for s in course.get_users(enrollment_type=["teacher", "student", "student_view", "ta", "observer", "designer"])]
sidToName = {s.sis_user_id:s.name for s in users}
canvasIdToStudentID = {u.id:u.sis_user_id for u in users}
studentIdToCanvasId = {u.sis_user_id:u.id for u in users}


print("Clearing late days...")
# Iterate through all submissions 
for submission in assignmentObject.get_submissions():
    if submission.late:
        print("Late submission: ", submission.user_id)
        name = sidToName[canvasIdToStudentID[submission.user_id]]
        print(name)
        removeSubmissionLate(submission.user_id, assignmentObject)

print("Done!")    

