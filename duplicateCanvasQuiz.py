#!/usr/bin/python3
import sys
from canvasapi import Canvas
from CanvasSettings import *

if len(sys.argv) != 3:
    print(f"Arguments:  quizid copies")
    exit()

quizid = sys.argv[1]
copies = int(sys.argv[2])

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

# Get the quiz
quiz = course.get_quiz(quizid)

# Get the quiz questions
questions = [q for q in quiz.get_questions()]

# Create the new quizzes
for i in range(copies):
    title=f"{quiz.title} - Copy {i+1}"

    # Create a dictionary of quiz data from the existing quiz
    quizData = {
        "title": title,
        "description": quiz.description,
        "quiz_type": quiz.quiz_type,
        "assignment_group_id": quiz.assignment_group_id,
        "time_limit": quiz.time_limit,
        "shuffle_answers": quiz.shuffle_answers,
        "hide_results": quiz.hide_results,
        "show_correct_answers": quiz.show_correct_answers,
        # show_correct_answers_last_attempt
        "show_correct_answers_at": quiz.show_correct_answers_at,
        "hide_correct_answers_at": quiz.hide_correct_answers_at,
        "allowed_attempts": quiz.allowed_attempts,
        "scoring_policy": quiz.scoring_policy,
        "one_question_at_a_time": quiz.one_question_at_a_time,
        "cant_go_back": quiz.cant_go_back,
        "access_code": quiz.access_code,
        "ip_filter": quiz.ip_filter,
        "due_at": quiz.due_at,
        "lock_at": quiz.lock_at,
        "unlock_at": quiz.unlock_at,
        "published": quiz.published,
        "one_time_results": quiz.one_time_results,
        "only_visible_to_overrides": quiz.only_visible_to_overrides,
    }

    newquiz = course.create_quiz(quizData)

    # Add the questions to the new quiz
    for q in questions:
        # Create a dictionary of all the question data 
        qData = {
            "question[question_name]": q.question_name,
            "question[question_text]": q.question_text,
            # Group ID?
            "question[question_type]": q.question_type,
            "question[position]": q.position,
            "question[points_possible]": q.points_possible,
            "question[correct_comments]": q.correct_comments,
            "question[incorrect_comments]": q.incorrect_comments,
            "question[neutral_comments]": q.neutral_comments,
            # Text after answers
            "question[answers]": q.answers,
        }
        newquiz.create_question(**qData)
