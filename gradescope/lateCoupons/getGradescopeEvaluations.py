import requests
import zipfile
import io
import re
import csv

def getGradescopeEvaluations(user, password, courseId, assignmentId):
    """Returns a dictionary representing the grading of all items in an assignment.

    Args:
        user (str): Email (login) of user
        password (str): Password of user
        courseId (int): Unique integer for course (from URL)
        assignmentId (int): Unique ID for assignment (from assignment URL)

    Returns:
        dict: dictionary of dictionaries: Assignment part to students or misc.  Students are a dict keyed by student ID with field for all elements of grading for the part
    """
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
    t = session.get(f'https://www.gradescope.com/courses/{courseId}/assignments/{assignmentId}/export_evaluations')

    grading = {}

    # Open zip file
    fp = io.BytesIO(t.content)
    z = zipfile.ZipFile(fp, "r")
    # Iterate over each file in the list
    for f in z.filelist:
        if f.orig_filename.endswith(".csv"):
            # Strip of up to / (dir/assignment) and ".csv"
            part = f.orig_filename.split('/')[-1][0:-4]
            grading[part] = {}
            grading[part]["students"] = {}
            grading[part]["misc"] = {}
            data = z.read(f)
            str_data = data.decode()
            c=csv.reader(io.StringIO(str_data), quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL)
            lines = [l for l in c]
            keys = lines[0]
            for l in lines[1:]:
                # Student record
                rec = dict(zip(keys, l))
                # Try to get the student ID
                if SID := rec.get('SID'):
                    # Add it to the grading record
                    grading[part]["students"][SID] = rec
                elif len(l)>0:
                    grading[part]["misc"][l[0]] = rec

    return grading  