# Summary

These scripts synchronize late days between Gradescope and Canvas and then utilize the Canvas late penalty. 
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

# 3. Assignment Data

This needs to be updated for each assignment (each time relevant scripts are run).

## 3.1 Assignment Items 

Update the `assignment` ID of the relevant items in Canvas and Gradescope.

ID numbers come from the relevant URL of the assignments in both Gradescope and Canvas URLs.  

```
assignment= {
    "GradescopeID": TODO,
    "CanvasID": TODO
}
```
For example, if the URL for the assignment on Gradescope is: https://www.gradescope.com/courses/707724/assignments/4369250/outline/edit, the `GradescopeID` is 4369250.  And if the corresponding Assignment page in Canvas has the URL https://wustl.instructure.com/courses/122301/assignments/621264?module_item_id=2080845, the `CanvasID` is 621264.

# Scripts

`computeAndApplyCoupons` will use the values in `AssignmentData.py` (and `CanvasSettings.py`) to retrieve the data for the specified assignment, compute the number of late days, and apply them to the Canvas gradebook. 

Running it more than once:
* May duplicate comments.  
* May increase "Late days". 
* Can not rescind / reduce the number of late days from a prior run.

`emailsOfLates` will retrieve the email addresses of anyone who has not submitted the assignment yet. This can be used to notify students that at least one part of the assignment is unsubmitted.

`getGradingCompletion` can be used to retrieve data about the grading progress and TA effort in grading. 

