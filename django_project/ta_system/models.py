from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_num = models.CharField(max_length=14, unique=True, verbose_name="Course Number (e.g. CSCI110101)")
    name = models.CharField(max_length=60)
    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, blank=True)
    days_of_week = models.CharField(max_length=10, verbose_name="Days of the Week (e.g. M/W/F)")
    start_time = models.TimeField(verbose_name="Start Time (e.g. 14:00)")
    end_time = models.TimeField(verbose_name="End Time (e.g. 14:50)")
    building = models.CharField(max_length=30)
    room_number = models.CharField(max_length=5)
    max_num_tas = models.PositiveIntegerField(default=2, verbose_name="Max Number of TAs")
    num_tas = models.PositiveIntegerField(default=0, verbose_name="Number of TAs")

    def __str__(self):
        return f'{str(self.course_num)}: {self.name}'


class Instructor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def first_name(self):
        if ' ' in self.name:
            return self.name.split(' ')[0]
        return self.name

    def last_name(self):
        if ' ' in self.name:
            return self.name.split(' ')[1]
        return self.name

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    eagle_id = models.PositiveSmallIntegerField(null=True, blank=True)
    courses_taken = models.ManyToManyField(Course, related_name="students", blank=True)
    ta_assignments = models.ManyToManyField(Course, related_name="tas", blank=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
