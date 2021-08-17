#!/usr/local/bin/python3
# TODO: Update above if needed

import sys
from canvasapi import Canvas
import json  # For files
import datetime
import sys   # sys.stdout and sys.argv
from CanvasSettings import *  # Import COURSE_ID, API_URL, API_KEY


# NOTES: Overrides seem to work for quizzes, but not other assignments (on beta instance)


####### DEBUGGING
# import logging

# logger = logging.getLogger("canvasapi")
# handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# handler.setLevel(logging.DEBUG)
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)
########


#  Check for arguments
if len(sys.argv)!=2:
    print(f"Arguments:  json file of data")
    exit(1)   

data = json.load(open(sys.argv[1]))

# Convert a local date/time string into a valid format for Canvas (ISO 8601)
def convertTime(time):
    if time in [None, ""]:
        return ""
    dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    return dt.isoformat()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

# Get all the sections (needed if there are section-specific overrides)
sections = {s.name:s for s in course.get_sections()}

if "assignments" in data:
    # Get the Canvas assignments as a dictionary by name
    assignments = {a.name:a for a in course.get_assignments()}    
    # Iterate through the assignment data in the file
    for (aname, adata) in data["assignments"].items():
        if aname in assignments: # Confirm it's in Canvas
            print(f"------ Assignment: {aname} ----------")
            assign = assignments[aname]
            opts = dict()
            opts["assignment[name]"] = aname
            opts["assignment[due_at]"] = convertTime(adata.get("due_at"))
            opts["assignment[unlock_at]"] = convertTime(adata.get("unlock_at"))
            opts["assignment[lock_at]"] = convertTime(adata.get("lock_at"))
            results = assign.edit(**opts)

            # Deal with overrides
            if "overrides" in adata:
                # Get the existing overrides
                overrides = {o.title:o for o in assign.get_overrides()}
                for (oname, odata) in adata["overrides"].items():
                    if oname not in sections:
                        print(f"Error: '{oname}' is not a valid section name", file=sys.stderr)
                    else:
                        # Creating or updating 
                        if oname in overrides:  # Updating existing override
                            newOverride = dict()
                            newOverride["assignment_override[due_at]"] = convertTime(odata.get("due_at"))
                            newOverride["assignment_override[unlock_at]"] = convertTime(odata.get("unlock_at"))
                            newOverride["assignment_override[lock_at]"] = convertTime(odata.get("lock_at"))
                            c_over = overrides[oname]
                            result = c_over.edit(**newOverride)
                        else:  # Creating a new override
                            newOverride = dict()
                            newOverride["title"] = oname
                            newOverride["due_at"] = convertTime(odata.get("due_at"))
                            newOverride["unlock_at"] = convertTime(odata.get("unlock_at"))
                            newOverride["lock_at"] = convertTime(odata.get("lock_at"))
                            newOverride["course_section_id"] = sections[oname].id
                            assign.create_override(assignment_override=newOverride)
        else:  # Wasn't in Canvas --- error
            print(f"Error: '{aname}' is not the title of an Assignment on Canvas", file=sys.stderr)

if "page todo dates" in data:
    pages = {p.title:p for p in course.get_pages()}

    for (pname, pdate) in data.get("page todo dates", dict()).items():
        if pname in pages:
            page = pages[pname]
            newTime = convertTime(pdate)
            print(f"------ To-Do for: {pname} ----------")
            # page.edit(**{"wiki_page[student_todo_at]":newTime, "wiki_page[todo_date]":newTime})
            page.edit(**{"wiki_page[student_todo_at]":newTime})
        else:
            print(f"Error: '{pname}' is not the title of a page on Canvas", file=sys.stderr)

