from django.db import models
from django.contrib.auth.models import User
from ta_system.data_formats.course_data_formats import DATA_FORMATS as COURSE_DATA_FORMATS
from ta_system.data_formats.applicant_data_formats import DATA_FORMATS as APPILCANT_DATA_FORMATS
from .validators import DataValidator


class Course(models.Model):
    semester = models.ForeignKey('Semester', on_delete=models.SET_NULL, null=True, blank=True)
    course_number = models.CharField(max_length=10, verbose_name="Course Number (e.g. CSCI110101)",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['course_number'], 
            message="Please enter a valid full course number, e.g. 'CSCI110101'."
        )]
    )
    name = models.CharField(max_length=60,
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['name'], 
            message="Please enter the name of the course, e.g. 'Computer Science I'."
        )]
    )
    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, blank=True)
    days_of_week = models.CharField(max_length=13, verbose_name="Days of the Week (e.g. M/W/F)",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['days_of_week'], 
            message="Please specify the days of the week this class meets separated by slashes, e.g. 'M/W/F'."
        )]
    )
    start_time = models.TimeField(verbose_name="Start Time (e.g. 14:00)",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['start_time'], 
            message="Please enter the time this class starts (in millitary time), e.g. '14:00'."
        )]
    )
    end_time = models.TimeField(verbose_name="End Time (e.g. 14:50)",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['end_time'], 
            message="Please enter the time this class ends (in millitary time), e.g. '14:50'."
        )]
    )
    building = models.CharField(max_length=30,
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['building'], 
            message="Please enter the building this class meets in, e.g. 'Fulton'."
        )]
    )
    room_number = models.CharField(max_length=6,
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['room_number'], 
            message="Please enter the number of the room this class meets in, e.g. '250'. One letter building codes may be included, e.g. '250S'."
        )]
    )
    max_num_tas = models.PositiveIntegerField(default=2, verbose_name="Max Number of TAs",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['max_num_tas'], 
            message="Please enter the maximum number of TAs that can be assigned to this course, e.g. '3'. This field defaults to '2'."
        )]
    )
    assigned_tas = models.ManyToManyField('Profile', related_name="ta_courses", verbose_name="Assigned TAs", blank=True)

    class Meta:
        unique_together = ('semester', 'course_number')

    def __str__(self):
        semester = self.semester if self.semester else 'NO SEMESTER'
        return f'{semester}: {self.course_number} – {self.name}'


class Semester(models.Model):
    semester = models.CharField(max_length=5, unique=True, verbose_name="Semester (e.g. 2020F)",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['semester'],
            message="Please specify the year followed by the semester, e.g. '2020F'."
        )]
    )

    def __str__(self):
        return self.semester


class Instructor(models.Model):
    name = models.CharField(max_length=60, unique=True,
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['instructor'], 
            message="Please enter the name of the Instructor, e.g. 'Robert Muller'."
        )]
    )

    def first_name(self):
        if ' ' in self.name:
            return self.name.split(' ')[0]
        return self.name

    def last_name(self):
        if ' ' in self.name:
            return self.name.split(' ')[-1]
        return self.name

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    eagle_id = models.CharField(max_length=8, unique=True, null=True, blank=True,
        validators=[DataValidator(
            regex=APPILCANT_DATA_FORMATS['eagle_id'], 
            message="Please enter a valid 8-digit eagle id, e.g. '58704254'."
        )]
    )
    courses_taken = models.ManyToManyField(Course, related_name="students", blank=True)

    def __str__(self):
        return f'{self.eagle_id}: {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
