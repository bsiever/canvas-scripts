#!/usr/local/bin/python3
import sys
from canvasapi import Canvas
from string import Template

from CanvasSettings import *

import json  # For making due dates into map
import datetime


### THIS VERSION WILL LOCK assignment (not accepted after)
#### Should be used for quizzes / surveys


if len(sys.argv)!=2:
    print(f"Arguments:  JSONFileName")
    exit(1)   

# Open the schedule
with open(sys.argv[1]) as json_file:
    schedule = json.load(json_file)

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)
sectionNamesToIds = {i.name:i.id for i in course.get_sections()}

# Iterate through the schedule
for assignment in schedule:
    # Get the assignment
    match = False
    for a in course.get_assignments(**{"search_term":assignment}):
        if a.name == assignment:
            print(f'Updating: {assignment}')
            match = True
            if isinstance(schedule[assignment], dict):
                for sect,date in schedule[assignment].items():
                    try: 
                        dueDate =  datetime.datetime.strptime(date, '%Y-%m-%d %I:%M%p').isoformat()
                    except: 
                        print(f'Invalid due date for {assignment}: {date}')
                        continue

                    if sect in sectionNamesToIds:
                        section = sectionNamesToIds[sect]
                        # If an override already exists, delete it.
                        for o in a.get_overrides():
                            if hasattr(o, 'course_section_id') and o.course_section_id == section: 
                                o.delete()
                        # No existing override (now).  Add one    
                        arg = {"assignment_override[course_section_id]":str(section),"assignment_override[due_at]":dueDate,"assignment_override[lock_at]":dueDate}
                        a.create_override(**arg)
                    else:
                        print(f'Invalid Section name: {section}')
                        continue 

            elif isinstance(schedule[assignment], str):
                try: 
                    dueDate = datetime.datetime.strptime(schedule[assignment], '%Y-%m-%d %I:%M%p').isoformat() 
                except: 
                    print(f'Invalid due date for {assignment}')
                    continue
                # Try to update it
                a.edit(**{"assignment[due_at]":dueDate})
                a.edit(**{"assignment[lock_at]":dueDate})

    if match == False:
        print(f'No matching assignment for {assignment}')           