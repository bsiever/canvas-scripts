# Summary

These scripts help manage true 0-penalty "Late Coupons" by handling the accounting of coupons between Gradescope and Canvas.  They do not "reject" credit when there are insufficient coupons, but they do print a list of any students who don't have sufficient coupons.

# 1. Setup for Canvas

## 1a. Install the Canvas Python API

https://github.com/ucfopen/canvasapi
(`pip install canvasapi`)

## 1b. Update CanvasSettings.py

### COURSE_ID

The course ID is the number in the course URL.   Browse to the course and extract the number.  For example, it would be the 
24032 in https://wustl.instructure.com/courses/24032 

For example, the 
```
COURSE_ID = TODO  
```
would be changed to:
```
COURSE_ID = 24032
```

### API_KEY

Create an API key via your User Settings at https://wustl.instructure.com/profile/settings .  (INstructions: https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-manage-API-access-tokens-as-an-instructor/ta-p/1177)

(API keys are strings and should be in double quotes)

### API_URL

Update the API URL for your institutions Canvas instance. You may want to test work on a "test" instance. 

# 1c. Gradebook / Grade Entry

A. Create a 0-credit assignment called "Remaining Late Lab Coupons" (script searches for that exact name).  

B. Set the default score to the number of coupons you'd like. (See: https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-set-a-default-grade-for-an-assignment-in-the-Gradebook/ta-p/747).  Be sure to set it to a value greater than 0.

# 2. Gradescope 

## 2a. Course Access (`gradescope` in `LabData.py`)

Update the LabData.py scrpt's `gradescope` section with :
1. Create an email alias account and add it to the course as a TA. For example, create a "graderbot@myemaildomain.org" type account and a unique, hard password.  
2. The `courseID` number.  This is the number in the URL of the course on Gradescope.   For example, it's the 707724 in https://www.gradescope.com/courses/707724. 
3. Update the `login` and `password` with the email credentials created in step 1. 

# 3. Assignment Data (`LabData.py`)

This section of `LabData.py` needs to be updated for each assignment (each time relevant scripts are run).

## 3.1 Title

Update the title, which is used in comments added to Canvas:
```
assignmentTitle = "TODO"  # Used in messages
```
## 3.2 Assignment Parts 

Update the `assignmentParts` JSON with the names and details of individual parts.  If there are multiple parts, the coupons will be the maximum of all possible parts.

ID numbers come from the relevant URL of the assignments in both Gradescope and Canvas URLs.  

```
assignmentParts= {
    "Part 1": {
        "GradescopeID": TODO,
        "CanvasID": TODO
    },
    "Part 2": {
        "GradescopeID": TODO,
        "CanvasID": TODO
    }
    # , ...
}
```
For example, if "Part 1" on Gradescope had the URL: https://www.gradescope.com/courses/707724/assignments/4369250/outline/edit, the `GradescopeID` is 4369250.  And if the corresponding Assignment page in Canvas has the URL https://wustl.instructure.com/courses/122301/assignments/621264?module_item_id=2080845, the `CanvasID` is 621264.

# Scripts

`computeAndApplyCoupons` will use the values in `LabData.py` (and `CanvasSettings.py`) to retrieve the data for the specified assignment, compute the number of late coupons, and apply them to the Canvas gradebook. 

**This should not be run more than once!** It does not check for prior updates of the same assignment and would result in multiple deductions!  It should only be run once after the final date that Gradescope accepts work. 

**It only updates coupons, not credit**.  Credit still muse be synchronized with Gradescope via the traditional "push" of grades. 

**Out of Coupons** The script prints any cases where students have insufficient coupons (i.e., would "go negative" if accepted), but don't actually deduct coupons.  You must manually review such cases and either notify students and zero grades, or accept assignments and manually update coupons to acknowledge any sort of late penalty. 

`emailsOfLates` will retrieve the email addresses of anyone who has not submitted the assignment yet. This can be used to notify students that at least one part of the assignment is unsubmitted.

`getGradingCompletion` can be used to retrieve data about the grading progress and TA effort in grading. 

Update 
```
data = getGradescopeEvaluations(gradescope["login"], gradescope["password"], gradescope["courseID"], TODO) # TODO: Replace TODO with string of assignment ID (from assignment URL)
```
with the appropriate assignment ID from Gradescope and run it.  It will return a CSV of details on grading efforts. 

# Late Coupon Notifications

After running the scripts it is nice to use the Canvas "Notify students who" feature (https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-send-a-message-to-students-from-the-Gradebook/ta-p/741) to:
1. Warn about being low on late coupons (i.e., notify students who Scored less than 7 on Late coupons (have fewer than 7))
2. Warn students who are out of late coupons (Scored less than 1)
   