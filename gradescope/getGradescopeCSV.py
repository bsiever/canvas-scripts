import requests
import re
import json

def getGradescopeCSV(user, password, courseId, assignmentId):
    session = requests.Session()
    # Get the initial page to get a csrf token
    p = session.get('https://www.gradescope.com')

    at = re.search('csrf-token" content="([^"]*)', p.text)
    token = at.group(1)

    # Create the payload for login
    payload = { 'utf8':"%E2%9C%93",
                'authenticity_token':token,
                'session[email]':user, 
                'session[password]':password,
                'session[remember_me]':0,
                'commit':'Log In',
                'session[remember_me_sso]':'0'
                }

    # Post the payload / log in to site
    s = session.post("https://www.gradescope.com/login", data=payload)

    # Get the CSV for the course/assignment
    t = session.get(f'https://www.gradescope.com/courses/{courseId}/assignments/{assignmentId}/scores.csv')

    return t.text



def openSession(user, password):
    session = requests.Session()
    # Get the initial page to get a csrf token
    p = session.get('https://www.gradescope.com')

    at = re.search('csrf-token" content="([^"]*)', p.text)
    token = at.group(1)

    # Create the payload for login
    payload = { 'utf8':"%E2%9C%93",
                'authenticity_token':token,
                'session[email]':user, 
                'session[password]':password,
                'session[remember_me]':0,
                'commit':'Log In',
                'session[remember_me_sso]':'0'
                }

    s = session.post("https://www.gradescope.com/login", data=payload)
    return session, token



def getMemberships(session, token, courseId):
    # Create the payload for new ID 
    payload = { 'utf8':"%E2%9C%93",
                'authenticity_token':token
        }

    memberships = session.get(f'https://www.gradescope.com/courses/{courseId}/memberships', data=payload)
    return memberships.text




def updateID(session, token, courseId, membershipId, newSID):
    # Patch ID
    # Create the payload for new ID 
    payload = { 'utf8':"%E2%9C%93",
                'authenticity_token':token,
                'course_membership[sid]':newSID 
                }

    t = session.patch(f'https://www.gradescope.com/courses/{courseId}/memberships/{membershipId}', data=payload)

    return t.text

def getIDs(memberships):
    # Parse out all the buttons with class rosterCell--editColumnIcon ; Create a map of data-id to a record that includes the 
    # data-cm,  data-email, data-lms-user-id 
    ids = {}
    lines = memberships.split("\n")
    for line in lines:
        if 'rosterCell--editColumnIcon' in line:
            cm = re.search('data-cm="([^"]*)"', line)
            # Replace the quot&; in cm with a " and then convert the json strong to a record
            if cm:
                m = re.search('data-id="([^"]*)"', line)
                email = re.search('data-email="([^"]*)"', line)
                lms = re.search('data-lms-user-id="([^"]*)"', line)
                cm = cm.group(1)
                cm = cm.replace('&quot;','"')
                cm_dict = json.loads(cm)
                cm_dict['email'] = email.group(1) if email else ''
                cm_dict['lms-id'] = lms.group(1) if lms else ''
                cm_dict['gradescope-id'] = m.group(1) if m else ''
                cm_dict['cm-text'] = cm
                ids[m.group(1)] = cm_dict
            else:
                print("No cm for " + line)
    # Returns a map of gradescope-id to a record with email, lms-id, sid, gradescope-id, cm-text
    return ids


def updateStudentId(session, token, courseId, membershipId, newSID):
    # Patch ID
    # Create the payload for new ID 
    payload = { 'utf8':"%E2%9C%93",
                'authenticity_token':token,
                'course_membership[sid]':newSID 
                }

    t = session.patch(f'https://www.gradescope.com/courses/{courseId}/memberships/{membershipId}', data=payload)

    return t.text

