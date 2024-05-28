#!/usr/local/bin/python3

from getGradescopeCSV import getGradescopeCSV
from canvasapi import Canvas
from CanvasSettings import *
from LabData import * 

from canvasUpdates import *
from functools import reduce
import csv

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

# Get all the late coupon info
canvasLateCouponAssignment = course.get_assignments(search_term	="Remaining Late Lab Coupons")[0]
defaultLateCoupons = int(canvasLateCouponAssignment.points_possible)

# Get handy data for users and a map of submissions
users = [s for s in course.get_users(enrollment_type=["teacher", "student", "student_view", "ta", "observer", "designer"])]
canvasIdToStudentID = {u.id:u.sis_user_id for u in users}
studentIdToCanvasId = {u.sis_user_id:u.id for u in users}
studentIdToEmail = {u.sis_user_id:u.email for u in users}

# Get all the current coupons & comments
# submissions = [s for s in  canvasLateCouponAssignment.get_submissions(include=["submission_comments"])]
# sidToSubmission = {canvasIdToStudentID[s.user_id]:s for s in submissions}
sidToName = {s.sis_user_id:s.name for s in users}

# # Coupon tag:  "LAB N:"
# def lateCouponMessage(part, message=None):
#     # Prefix on both paths need to exactly match
#     if message:
#         return f'{assignmentTitle}: {part} - {message}'
#     else:
#         return f'{assignmentTitle}: {part}'

# def checkForTag(part, comment):
#     # Needs to exactly match prefix above
#     return comment.startswith(f'{assignmentTitle}: {part}')

def timeToSeconds(time):
    # No submission
    if time==None:
        return -1
    times = time.split(":")
    time = int(times[2]) + int(times[1])*60 + int(times[0])*60*60
    return time if time>60 else 0

# get CSVs from gradescope:
IDsToLate ={}  # Map of studentID:map of late;  Map of late is "Part Title":"time" (in seconds)
print("Getting CSV Data from Gradescope")
for (part, dets) in assignmentParts.items():
    # Read it all in 
    data = getGradescopeCSV(gradescope["login"], gradescope["password"], gradescope["courseID"], dets["GradescopeID"])
    read = csv.DictReader(data.splitlines())
    # For each item, add/update the dictionary of late data
    for r in read:
        SID = r["SID"]
        lateData = IDsToLate.get(SID, {})
        time = timeToSeconds(r["Lateness (H:M:S)"])
        lateData[part] = time
        IDsToLate[SID] = lateData
    # Also read in the Canvas data for the part
    canvasIdForPart = assignmentParts[part]["CanvasID"]
    print(f"Getting canvas assignment part: {part} {canvasIdForPart}")
    assignmentParts[part]["Canvas Assignment"] = course.get_assignment(canvasIdForPart)
    # print(assignmentParts[part]["Canvas Assignment"].name)

# Iterate through Lates by student ID
print(f"Emails with at least one unsubmitted part {assignmentTitle}")
for sid in IDsToLate:
    name = sidToName.get(sid, None)
    email = studentIdToEmail.get(sid, None)
    parts = IDsToLate.get(sid, None)
    latest = reduce(lambda a,b: a if a<b else b, parts.values())
    # If any part is unsubmitted:
    if latest==-1:
        print(f"{email}")

