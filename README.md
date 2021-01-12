# Description

This Python script is basically written for CENG 443 Fall 2021 Course Homework 3 and it generates random input files to be consumed by students.

# Usage

It basically takes three optional arguments and/or parameters, namely `--location` or `-l` for where to create files, `--student-count` or `-sc` for number of students to be generated and `--fail-possible` or `--fail-not-possible` to decide whether allow students to fail in any course.

User can also obtain info with `--help` or `-h` parameter.

# File Contents

`course_codes_and_terms.json`: It basically has course info that this input generator depends on and it will use all courses in that file and generate exams of students accordingly. The fields are self-explanatory.
`names_of_exams.json`: Name of the possible exams that is allowed to be generated.
`student_name_surnames.json`: A database to generate Turkish names and surnames.
`years.json`: Possible registration years for the students.