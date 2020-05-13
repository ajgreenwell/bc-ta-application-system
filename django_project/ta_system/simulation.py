

def assign_TA(applicant, course):
    if course.course_number in applicant.courses_taken:
        if count(applicant.ta_assignments) == 0:
            num_tas = num_tas + 1
            course.teaching_assistants.add(applicant)
            applicant.ta_assignments.add(course)


def convert_day_to_number(day):
    if day == "U":
        return 0
    elif day == "M":
        return 1
    elif day == "T":
        return 2
    elif day == "M":
        return 3
    elif day == "R":
        return 4
    elif day == "F":
        return 5
    elif day == "S":
        return 6
    else:
        #messages.error(request, 'You have entered an one digit day codes for days of week of the course')
        return -99999


def convert_days_of_week(days_of_week):
    col = []
    if len(days_of_week) == 3:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
    elif len(days_of_week) == 5:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        day3 = days_of_week.split('/')[2]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
        col.append(convert_day_to_number(day3))
    elif len(days_of_week) == 1:
        col.append(convert_day_to_number(days_of_week))
    else:
        col.append(-1)
        # slash_count = 0
        # position = days_of_week.find('/')
        # result = 4
    return (col)


def convert_class_time(start, end):

    return(result)


def check_availability(col, row, availability):
    return True
