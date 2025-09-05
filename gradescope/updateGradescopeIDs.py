import getGradescopeCSV
import re
import json

# TODO
# user = 
# password = 
# courseID = 
(session, token) = getGradescopeCSV.openSession(user, password)

memberships = getGradescopeCSV.getMemberships(session, token, courseID)

idmap = getGradescopeCSV.getIDs(memberships)

# Create a map of sid to gradescope-id
sidmap = {}
for (k,v) in idmap.items():
    sidmap[v['sid']] = v['gradescope-id']


# Update a student using their OLD id to change it to a new one
oldID = "12345" 
gradescopeId = sidmap[oldID] 
getGradescopeCSV.updateStudentId(session, token, courseID, gradescopeId, "7718")

# TODO
# Open CSV of universal IDs and SIS IDs, then loop through and convert each Universal to Gradescope ID and do an update with the SIS ID

