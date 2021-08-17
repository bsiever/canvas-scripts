# Convenience Scripts for Working with Canvas

These scripts support:

1. Updating dates in Canvas (assignment/quiz available, due, and lock dates and todo items). 
2. Getting a list of emails, which can be used to contact students or update external tools, like Piazza.

## One-time setup

You'll need to install the Python Canvas API.  For me it was something like `pip3 install canvasapi​`. See https://github.com/ucfopen/canvasapi

Update the three scripts, `getCourseSchedule.py`, `putCourseSchedule.py`, and `getStudentEmailsForPiazza.py` so the `#!...python...` at the top reflects your installation of Python.

# Initial setup

1. Copy over scripts to a new directory/location for the current class.
2. Update `CanvasSettings.py` script (it includes instructions for what is needed) for the current semester.  It has three values that are used by other scripts:
   * `COURSE_ID` A course/offering specific ID (changes for each course each semester). **BE SURE TO UPDATE THIS IMMEDIATELY FOR EACH SEMESTER** (You don't want to accidentally update values for the prior offering of the course)
   * `API_URL`: The URL of the Canvas server to use.  I usually test things on the "beta" version of Canvas first and then update this for the production version.  The Beta version is not visible to students and is overwritten by the live version on weekends.  Test things on the first few uses by trying them out on beta.  
   * `API_KEY`:  An API key (this can be the same for every course --- when you create it you can specify an expiration date).  Be sure to never share this or expose it.  Do NOT ever add updates to `CanvasSettings.py` to a git commit/etc. (It's added to `.gitignore` to help avoid this).  This doesn't need to be changed every semester.
3. Setup initial course shell in Canvas (probably by copying over all data from a prior instance of the course and maybe merging/[cross-listing](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-cross-list-a-section-in-a-course-as-an-instructor/ta-p/1261) multiple sections into a single course shell).
4. Run `getCourseSchedule.py` script, which will get all dates and dump them into a .json file (the output file can be given as a command line argument or, if no are, it defaults to stdout) I like to watch it work, so I usually do: `./getCourseSchedule.py | tee schedule.json​`.  This step can be repeated each semester if there are significant changes to the course structure (changes to number/types of assignments or names used for assignments or pages with to-do times). 
5. Edit / rearrange the resulting JSON.  It's not usually in the order of course content, so I juggle it a bit and update expected dates.  

# JSON File Structure

Here's an example of what the JSON file may look like.  *Comments (`#`) are not allowed, but are added to indicate details*:

```
{   # The "Assignments" group will include Canvas Quizzes and Assignments
    "assignments": {
        "Assignment 1": {                           # The exact name of the assignment
            "due_at": "2021-03-18 23:59:59",        # When it's due (see below)
            "lock_at": null,                        # The hard cut-off (see below)
            "unlock_at": null                       # When it becomes available (see below)
        },
        ...
        "Quiz N": {
            "due_at": null,
            "lock_at": null,
            "unlock_at": null
        }
    },
    # The "page todo dates" group can be used to indicate a page/item that should be reviewed by a particular date/time (it adds non-graded items to students Canvas calendar and to-do list)
    "page todo dates": {
        "Week 1 Reading": "2021-01-26 23:52:00",   # The exact page name and corresponding due date
        ...
        "Week N Pre-class Video": "2021-01-31 23:54:00",
        "Info Only: null
    }
}
```

Assignment items have three types of dates:

* `due_at`: This is when it's meant to be due.  If the course uses Canvas for submissiosn, like with Canvas-based quizzes, this is *NOT* a hard cutoff.
* `local_at`: This is the hard cutoff for Canvas-based submissions. If your course has a Canvas-enforced late submission policy, this may be longer than `due_at` or un-set.  If you want to enforce hard deadlines at the due date this should be the same date as the `due_at`.  Leaving it `null` will allow late submissions using whatever the Canvas late submission policy is (often defaults to no penalty!)
* `unlock_at`:  The "Available at" date of when the item will be visible to students.

# Regular Updates

1. Be sure that the `COURSE_ID` in `CanvasSettings.py` reflects the current semester!
   * It's highly recommended that you set the `API_URL` to the beta instance of Canvas for inital tests.  Remember that the beta instance may reflect the course as of the most recent weekend.  If necessary, you may be able to manually sync it by doing an export on the live instance and an import it on http://wustl.beta.instructure.com. 
2. Update the dates in the .json file from the setup process. The date format is `2021-07-12 23:59:59` in your local timezone.
3. Use `putCourseSchedule.py` to post the changes.  Give the .json file to use as the first command line argument.  (Ex: `./putCourseSchedule.py newSemester.json`).  
4. Check your calendar / course stream to quickly spot any problems.
5. If you were working from the beta instance and are happy with the results, update the `API_URL` and re-run the script to push to the production instance.
