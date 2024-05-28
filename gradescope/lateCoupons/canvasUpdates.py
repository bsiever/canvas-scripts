

from canvasapi import Canvas
from CanvasSettings import *

# Used by other scripts

def updateSubmissionLate(studentCanvasID, assignment, status, amount=0, comment=None):
    # Unit of amount is "seconds", but Canvas shows days.  Multiply by 86400 and round
    # Set submission[late_policy_status] = “late”, “missing”, “none”, or null.
    if not status in ["late", "missing", "none", None]:
        print(f"Invalid submission status {status}")
    else:
        submission = assignment.get_submission(studentCanvasID)
        data = {"late_policy_status":status, "seconds_late_override":amount}
        if comment:
            comments = {"text_comment":comment}
        else:
            comments = None
        submission.edit(submission=data, comment=comments)

def updateGrade(studentCanvasID, assignment, grade, comment=None):
    submission = assignment.get_submission(studentCanvasID)
    if comment:
        comments = {"text_comment":comment}
    else:
        comments = None
    submission.edit(submission={"posted_grade":grade}, comment=comments)
