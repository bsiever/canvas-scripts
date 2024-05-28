#!/usr/local/bin/python3

from getGradescopeEvaluations import getGradescopeEvaluations
from LabData import * 

# Get all the late coupon info
print("Getting CSV Data from Gradescope")

# TODO:  Use LabData's Assignment Parts and GradescopeID
data = getGradescopeEvaluations(gradescope["login"], gradescope["password"], gradescope["courseID"], TODO) # TODO: Replace TODO with string of assignment ID (from assignment URL)


parts =[k for k in data.keys()]

graders={}

# Iterate over all students and build map
for p in parts:
    students = data[p]['students']
    for s in students.keys():
        rec = students[s]
        grader = rec['Grader']
        if grader not in graders:
            graders[grader] = {}
        if p in graders[grader]:
            graders[grader][p] = graders[grader][p]+1
        else:
            graders[grader][p] = 1

# Print header
print("Grader,"+",".join(parts))
# Print TA tallies
for (TA, grading) in graders.items():
    if len(TA)==0:
        TA='Ungraded'
    stuff = [str(grading.get(p,0)) for p in parts]
    line = TA+","+",".join(stuff)
    print(line)