#!/usr/bin/env python3
import getGradescopeCSV
import re
import json
import csv
import sys

# TODO
user = "GRADESCOPE USER NAME"
password = "GRADESCOPE PASSWORD"

# Check command line args
if len(sys.argv) < 3:
    print("Usage: python updateGradescopeIDs.py <csvfile of full canvas gradebook> <courseID>")
    sys.exit(1)

# Open the file and read it in
csvfile = sys.argv[1]
courseID = sys.argv[2]
with open(csvfile, 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)


# Get a map of "SIS User ID" to "Integration ID" 
univ_to_studentid = {}
studentid_to_universal = {}
for row in rows:
    sid = row.get("SIS User ID", "").strip()
    integration_id = row.get("Integration ID", "").strip()
    if sid and integration_id:
        univ_to_studentid[sid] = integration_id
        studentid_to_universal[integration_id] = sid


# # Print it out
# for sid, integration_id in univ_to_studentid.items():
#     print(f"{sid} -> {integration_id}")

(session, token) = getGradescopeCSV.openSession(user, password)

memberships = getGradescopeCSV.getMemberships(session, token, courseID)

idmap = getGradescopeCSV.getIDs(memberships)

# Create a map of sid to gradescope-id
sidmap = {}
for (currentGradescopeSID,gradescopeID) in idmap.items():
    sidmap[gradescopeID['sid']] = gradescopeID['gradescope-id']


# Iterate through the SID map
for (currentGradescopeSID,gradescopeID) in sidmap.items():
    # if the sid is in the integration_to_sid map, print it out
    if currentGradescopeSID in studentid_to_universal:
        print(f"*** Already updated {currentGradescopeSID} -> {gradescopeID}")
    else:
        # Confirm we know their new ID
        if currentGradescopeSID not in univ_to_studentid:
            print(f"*** Don't know new ID for {currentGradescopeSID} skipping")
            continue
        newID = univ_to_studentid[currentGradescopeSID]
        print(f"Updating {currentGradescopeSID} to {newID}")
        getGradescopeCSV.updateStudentId(session, token, courseID, gradescopeID, newID)
