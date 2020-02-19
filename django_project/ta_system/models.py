from django.db import models


class Course(models.Model):
    course_num = models.OneToOneField('CourseNumber', on_delete=models.CASCADE, verbose_name="Course Number")
    name = models.CharField(max_length=60)
    instructor = models.ForeignKey('Instructor', on_delete=models.PROTECT)
    days_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    building = models.CharField(max_length=30)
    room = models.CharField(max_length=5)
    # semester = NOT IMPLEMENTED
    max_num_tas = models.PositiveIntegerField(default=2, verbose_name="Max Number of TAs")
    num_tas = models.PositiveIntegerField(default=0, verbose_name="Number of TAs")

    def __str__(self):
        return f'{str(self.course_num)}: {self.name}'


class Instructor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class CourseNumber(models.Model):
    course_code = models.CharField(max_length=6)
    course_num = models.CharField(max_length=6)
    section_num = models.CharField(max_length=2)

    def full_course_number(self):
        return f'{self.course_code}{self.course_num}{self.section_num}'

    def __str__(self):
        return f'{self.course_code}{self.course_num}.{self.section_num}'
