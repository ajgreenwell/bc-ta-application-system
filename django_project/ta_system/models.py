from django.db import models

class Course(models.Model):
    course_num =
    section_num =
    name = 
    professor =
    days_of_week =
    start_time =
    end_time =
    building =
    room = 
    max_num_tas =

    def full_course_number(self):
        f'{self.course_num}{self.section_num}'

    def __str__(self):
        return f'{self.full_course_number()}: {self.name}'