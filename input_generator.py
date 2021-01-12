import argparse
import json
import random
import os
from os import path
import shutil

FAIL_CHANCE = 0.05
PATH_SEPARATOR = '/'
EXAM_QUESTION_COUNTS = [10, 20, 25, 40, 50, 80]
EMPTY_CHANCE = 0.1

fp = open('./student_name_surnames.json', encoding='utf-8')
name_and_surnames = json.load(fp)
fp.close()

fp = open('./years.json', encoding='utf-8')
years = json.load(fp)
fp.close()

fp = open('./course_codes_and_terms.json', encoding='utf-8')
course_data = json.load(fp)
fp.close()

fp = open('./names_of_exams.json', encoding='utf-8')
exam_names = json.load(fp)
fp.close()

parser = argparse.ArgumentParser(description="Generates input files for CENG443 HW3")
parser.add_argument('--location', '-l', dest='location', action='store', default="./input", help="Folder location to generate files to (default: %(default)s)")
parser.add_argument('--student-count', '-sc', dest='student_count', action='store', type=int, default=50, help="Number of student records to be generated (default: %(default)s)")
parser.add_argument('--fail-possible', '-fp', dest='fail_possible', action='store_true', help="Check if fail is possible")
parser.add_argument('--fail-not-possible', '-fnp', dest='fail_possible', action='store_false', help="Check if fail is not possible")
parser.set_defaults(fail_possible=True)

args = parser.parse_args()

folder_location = args.location

if path.exists(folder_location):
    shutil.rmtree(folder_location)

os.mkdir(folder_location)
print('Folder created at {}!'.format(folder_location))

def createFile(first_line, second_line, exam, counter, min, error_range):
    third_line = "{}".format(exam)
    question_count = random.choice(EXAM_QUESTION_COUNTS)
    true_answer_prob = min + random.random() * error_range
    fourth_line = ""

    for _ in range(question_count):
        rand_float = random.random()

        if rand_float < EMPTY_CHANCE:
            fourth_line += 'E'
        elif rand_float < (EMPTY_CHANCE + true_answer_prob):
            fourth_line += 'T'
        else:
            fourth_line += 'F'

    fp = open('{}{}{}.txt'.format(folder_location, PATH_SEPARATOR, counter), 'w', encoding='utf-8')
    fp.write("\n".join([first_line, second_line, third_line, fourth_line]))
    fp.close()

year_student_pair = {}
student_per_year = int(round(float(args.student_count) / len(years)))
student_count = student_per_year * len(years)

# Create student data
for year in years:
    year_student_pair[year] = []

    for _ in range(student_per_year):
        first_name = random.choice(name_and_surnames['names'])
        last_name = random.choice(name_and_surnames['surnames'])
        student_no = random.randint(1000000, 9999999)

        year_student_pair[year].append({
            'first_name': first_name,
            'last_name': last_name,
            'student_no': student_no
        })

# Map it to a dict to easily access data afterhand
course_data_dictionary = {}
course_codes = []
for course in course_data:
    course_codes.append(course['code'])
    course_data_dictionary[course['code']] = {
        'expected': course['expected'],
        'terms': course['terms'],
        'credits': course['credits']
    }

counter = 1

for year in years:
    for student in year_student_pair[year]:
        first_line = "{} {} {}".format(student['first_name'], student['last_name'], student['student_no'])
        failed_courses = []

        for code in course_codes:
            is_failed = random.random() <= FAIL_CHANCE and args.fail_possible
            course_expected_semester = course_data_dictionary[code]['expected']
            course_taken_at = (year + course_expected_semester[0] - 1) * 10 + course_expected_semester[1]
            second_line = "{} {} {}".format(course_taken_at, code, course_data_dictionary[code]['credits'])

            if is_failed:
                failed_courses.append(code)

                for exam in exam_names:
                    createFile(first_line, second_line, exam, counter, 0.5, 0.2)
                    counter += 1
            else:
                for exam in exam_names:
                    createFile(first_line, second_line, exam, counter, 0.7, 0.3)
                    counter += 1

        for code in failed_courses:
            course_expected_semester = course_data_dictionary[code]['expected']
            course_opened_terms = course_data_dictionary[code]['terms']
            course_taken_at = 0

            if course_expected_semester[1] == 1:
                if 2 in course_opened_terms:
                    course_taken_at = (year + course_expected_semester[0] - 1) * 10 + 2
                else:
                    course_taken_at = (year + course_expected_semester[0]) * 10 + 1
            else:
                if 1 in course_opened_terms:
                    course_taken_at = (year + course_expected_semester[0]) * 10 + 1
                else:
                    course_taken_at = (year + course_expected_semester[0]) * 10 + 2

            second_line = "{} {} {}".format(course_taken_at, code, course_data_dictionary[code]['credits'])

            for exam in exam_names:
                createFile(first_line, second_line, exam, counter, 0.7, 0.3)
                counter += 1