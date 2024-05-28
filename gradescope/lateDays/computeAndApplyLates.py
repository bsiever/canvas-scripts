#!/usr/local/bin/python3

from getGradescopeCSV import getGradescopeCSV
from canvasapi import Canvas
from CanvasSettings import *
from AssignmentData import * 
from canvasUpdates import *
from functools import reduce
import csv

gracePeriod = 60   # One minute of grace

# Initialize a new Canvas object
print("Connecting to Canvas...")
canvas = Canvas(API_URL, API_KEY)
print("Getting course...")
course = canvas.get_course(COURSE_ID)

# # Get all the late coupon info
# print("Getting Remaining Late Coupons Assignment...")
# canvasLateCouponAssignment = course.get_assignments(search_term	="Remaining Late Lab Coupons")[0]
# defaultLateCoupons = int(canvasLateCouponAssignment.points_possible)

# Get handy data for users and a map of submissions
print("Getting User Data...")
users = [s for s in course.get_users(enrollment_type=["teacher", "student", "student_view", "ta", "observer", "designer"])]
sidToName = {s.sis_user_id:s.name for s in users}
canvasIdToStudentID = {u.id:u.sis_user_id for u in users}
studentIdToCanvasId = {u.sis_user_id:u.id for u in users}


def timeToSeconds(time):
    # No submission
    if time==None:
        return -1
    times = time.split(":")
    time = int(times[2]) + int(times[1])*60 + int(times[0])*60*60
    return time if time>60 else 0

# get CSVs from gradescope:
print("Getting CSV Data from Gradescope")
data = getGradescopeCSV(gradescope["login"], gradescope["password"], gradescope["courseID"], assignment["GradescopeID"])
IDsToLate ={}  # Map of studentID:late time in seconds (0 for on-time, -1 for no submission, >0 is seconds late); 
read = csv.DictReader(data.splitlines())
# For each item, add/update the dictionary of late data
for r in read:
    SID = r["SID"]
    IDsToLate[SID] = timeToSeconds(r["Lateness (H:M:S)"])

# Also read in the Canvas data for the part
canvasIdForAssignment = assignment["CanvasID"]
print(f"Getting canvas assignment: {canvasIdForAssignment}")
assignmentObject = course.get_assignment(canvasIdForAssignment)
print(assignmentObject.name)

print("Processing late days...")
# Iterate through Lates by student ID
for sid in IDsToLate:
    name = sidToName.get(sid, None)
    lateTimeInSeconds = IDsToLate[sid]
    # If any part is late:
    if lateTimeInSeconds>gracePeriod:
        timeInDays = (lateTimeInSeconds // (60*60*24)) + 1
        print(f"{name} is late {timeInDays} day(s)")
        comment = f'Late {timeInDays} day(s)'
        updateSubmissionLate(studentIdToCanvasId[sid], assignmentObject, "late", amount=lateTimeInSeconds, comment=comment)

print("Done!")    

