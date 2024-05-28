#!/usr/local/bin/python3


# TODO:  CSE 247 script....Not used now.    Partly edited....needs review/testing.

from getGradescopeCSV import getGradescopeCSV
from canvasapi import Canvas
from CanvasSettings import *
from AssignmentData import * 

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

# Read it all in 
data = getGradescopeCSV(gradescope["login"], gradescope["password"], gradescope["courseID"], assignment["GradescopeID"])
read = csv.DictReader(data.splitlines())
# For each item, add/update the dictionary of late data
for r in read:
    SID = r["SID"]
    IDsToLate[SID] = timeToSeconds(r["Lateness (H:M:S)"])

# Also read in the Canvas data for the part
canvasIdForPart = assignment["CanvasID"]
print(f"Getting canvas assignment: {part} {canvasIdForPart}")
assignmentObject = course.get_assignment(canvasIdForPart)
# print(assignmentParts[part]["Canvas Assignment"].name)

# Iterate through Lates by student ID
print(f"Emails with at least one unsubmitted part {assignmentObject.name}")
for sid in IDsToLate:
    name = sidToName.get(sid, None)
    email = studentIdToEmail.get(sid, None)
    late = IDsToLate.get(sid, None)
    # If any part is unsubmitted:
    if late==-1:
        print(f"{email}")

