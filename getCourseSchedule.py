#!/usr/local/bin/python3
# TODO: Update above if needed
import sys
from canvasapi import Canvas
import json  # For files
import datetime
import sys   # sys.stdout and sys.argv


from CanvasSettings import *  # Import COURSE_ID, API_URL, API_KEY

#  Check for arguments
if len(sys.argv)>2:
    print(f"Arguments:  file name to write to or none (and .json data written to stdout)")
    exit(1)   

if len(sys.argv)==2:
    # Check if no file and can be opened for writing
    f = open(sys.argv[1],"x")
else:
    f = sys.stdout

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

data = dict()

# Convert a UTC time to a date time object in the local time zone
def utcTimeStrToLocalDatetime(utcTime):
    if utcTime == None:
        return None
    # https://stackoverflow.com/questions/4563272/how-to-convert-a-utc-datetime-to-a-local-datetime-using-only-standard-library/13287083#13287083
    dt = datetime.datetime.strptime(utcTime, '%Y-%m-%dT%H:%M:%SZ')
    dateStr = dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
    return str(dateStr)[:-6]


# Get all data about assignments

assignments = [a for a in course.get_assignments()]
assignmentData = dict()
for a in assignments:
    name = a.name
    assignmentData[name] = dict() 
    assignmentData[name]["due_at"] = utcTimeStrToLocalDatetime(a.due_at)
    assignmentData[name]["lock_at"] = utcTimeStrToLocalDatetime(a.lock_at)
    assignmentData[name]["unlock_at"] = utcTimeStrToLocalDatetime(a.unlock_at)
    overrides = [o for o in a.get_overrides()]
    overidesDict = dict()
    for o in overrides:
        # Only get the section-level overrides (not individual students/etc.)
        if hasattr(o,"course_section_id"):
            forTitle = dict()
            forTitle["due_at"] = utcTimeStrToLocalDatetime(o.due_at)

            forTitle["lock_at"] = utcTimeStrToLocalDatetime(o.lock_at) if hasattr(o,"lock_at") else ""
            forTitle["unlock_at"] = utcTimeStrToLocalDatetime(o.unlock_at) if hasattr(o,"unlock_at") else ""
            overidesDict[o.title] = forTitle
    # Only add overrides if there was at least one
    if len(overidesDict)>0:
        assignmentData[name]["overrides"] = overidesDict

# Add to the overall data for the JSON
data["assignments"] = assignmentData

pages = [p for p in course.get_pages()]
todoDict = dict()
todoCount = 0
for p in pages:
    name = p.title
    todoDate = utcTimeStrToLocalDatetime(p.todo_date)
    if todoDate!=None:
        todoCount = todoCount+1 
    todoDict[name] = todoDate

# Save the data for the JSON (if there's at least one)
if todoCount>0:
    data["page todo dates"] = todoDict 

json.dump(data,f, default=str, indent=4, sort_keys=True)
f.close()
