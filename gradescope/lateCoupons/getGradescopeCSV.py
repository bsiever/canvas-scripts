import requests
import re

# Used by other scripts

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

