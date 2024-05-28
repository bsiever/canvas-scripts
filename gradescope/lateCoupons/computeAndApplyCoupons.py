#!/usr/local/bin/python3

from getGradescopeCSV import getGradescopeCSV
from canvasapi import Canvas
from CanvasSettings import *
from LabData import * 
from canvasUpdates import *
from functools import reduce
import csv



# Initialize a new Canvas object
print("Connecting to Canvas...")
canvas = Canvas(API_URL, API_KEY)
print("Getting course...")
course = canvas.get_course(COURSE_ID)

# Get all the late coupon info
print("Getting Remaining Late Coupons Assignment...")
canvasLateCouponAssignment = course.get_assignments(search_term	="Remaining Late Lab Coupons")[0]
defaultLateCoupons = int(canvasLateCouponAssignment.points_possible)

# Get handy data for users and a map of submissions
print("Getting User Data...")
users = [s for s in course.get_users(enrollment_type=["teacher", "student", "student_view", "ta", "observer", "designer"])]
canvasIdToStudentID = {u.id:u.sis_user_id for u in users}
studentIdToCanvasId = {u.sis_user_id:u.id for u in users}
# Get all the current coupons & comments
print("Getting Actual Late Coupons...")
submissions = [s for s in  canvasLateCouponAssignment.get_submissions(include=["submission_comments"])]
sidToSubmission = {canvasIdToStudentID[s.user_id]:s for s in submissions}
sidToName = {s.sis_user_id:s.name for s in users}

# Coupon tag:  "LAB N:"
def lateCouponMessage(part, message=None):
    # Prefix on both paths need to exactly match
    if message:
        return f'{assignmentTitle}: {part} - {message}'
    else:
        return f'{assignmentTitle}: {part}'

def checkForTag(part, comment):
    # Needs to exactly match prefix above
    return comment.startswith(f'{assignmentTitle}: {part}')

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
    print(f"Getting {part} from GradeScope")
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
    print(assignmentParts[part]["Canvas Assignment"].name)


print("Processing late coupons...")
# Iterate through Lates by student ID
for sid in IDsToLate:
    name = sidToName.get(sid, None)
    parts = IDsToLate.get(sid, None)
    latest = reduce(lambda a,b: a if a>b else b, parts.values())
    # If any part is late:
    if latest>0:
        additionalCouponNeeded = True  # Assume coupon used until otherwise
        # Get the canvas submission (if one)
        submission = sidToSubmission.get(sid, None)
        if submission:
            lateCouponsRemaining = int(submission.grade) if submission.grade!=None else defaultLateCoupons
            # Iterate through the parts and update each             
            # maxLate = 0   # "Most late" part for Late Coupon time
            for p in parts:
                # If this part is late...
                if parts[p] > 0:
                    partCanvasAssignment = assignmentParts[p]["Canvas Assignment"]
                    addCommentForItem = True  # Assume needs comment
                    for comment in submission.submission_comments:
                        if checkForTag(p, comment["comment"]):  # Check for existing comment
                            additionalCouponNeeded = False
                            addCommentForItem = False
                    timeInDays = (parts[p] // (60*60*24)) + 1
                    print(f'Late {p} {timeInDays} days: Student ID: {sid}; Name: {name} Updating canvas: {partCanvasAssignment.name}')
                    commentForThisItem = lateCouponMessage(p)
                    # Update the coupons
                    comment = commentForThisItem if addCommentForItem else None
                    # Use maxLate time for overall coupons
                    # maxLate = max(maxLate, timeInDays)
                    # Update comments on late coupons
                    if comment: 
                        updateSubmissionLate(studentIdToCanvasId[sid], canvasLateCouponAssignment, "none", amount=None, comment=comment)
                    # Also update the specific item
                    # Use part-specific time for each part
                    updateSubmissionLate(studentIdToCanvasId[sid], partCanvasAssignment, "late", amount=timeInDays*60*60*24, comment=comment)
            if additionalCouponNeeded:
                # Get current coupons
                if lateCouponsRemaining < timeInDays:
                    print(f'*** ERROR!!! Late Submission and no late coupons remaining: Student ID: {sid}; Name: {name}')
                else:
                    updateGrade(studentIdToCanvasId[sid], canvasLateCouponAssignment, lateCouponsRemaining-timeInDays, comment=None)
        else:
            print(f'*** ERROR!!!  No submission data for a late item; Student ID: {sid}; Name: {name}')
    
#   Check submission comments to see if it's already recorded
#   If NOT already recorded:
#      Check coupons
#      If 0:  
#           Print error and that grade should be zero
#           Force grade to 0
#      Else: 
#          Deduct Coupon / Update
#          Update comments
#          Update assignments

