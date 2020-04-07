from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from .validators import DataValidator
from .data_formats.course_data_formats \
    import DATA_FORMATS as COURSE_DATA_FORMATS
from .data_formats.applicant_data_formats \
    import DATA_FORMATS as APPILCANT_DATA_FORMATS
from django.utils.timezone import now


class Course(models.Model):
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    course_number = models.CharField(
        max_length=10,
        verbose_name="Course Number",
        help_text="A full BC course number, e.g. CSCI110101.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['course_number'],
            message="Please enter a valid full course number, e.g. 'CSCI110101'."
        )]
    )
    name = models.CharField(
        max_length=60,
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['name'],
            message="Please enter the name of the course, e.g. 'Computer Science I'."
        )]
    )
    instructor = models.ForeignKey(
        'Instructor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    days_of_week = models.CharField(
        max_length=13,
        verbose_name="Days of the Week",
        help_text="The 1-character days of the week this class meets, separated by slashes, eg. T/R.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['days_of_week'],
            message="M = Mon; T = Tues; W = Wed; R = Thurs; F = Fri; A = Sat; S = Sun... e.g. M/W/F"
        )]
    )
    start_time = models.TimeField(
        verbose_name="Start Time",
        help_text="The time of day this class begins in millitary time, e.g. 14:00.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['start_time'],
            message="Please enter the time this class starts (in millitary time), e.g. '14:00'."
        )]
    )
    end_time = models.TimeField(
        verbose_name="End Time",
        help_text="The time of day this class ends in millitary time, e.g. 14:50.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['end_time'],
            message="Please enter the time this class ends (in millitary time), e.g. '14:50'."
        )]
    )
    building = models.CharField(
        max_length=30,
        help_text="The building this class meets in, e.g. Fulton.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['building'],
            message="Please enter the building this class meets in, e.g. 'Fulton'."
        )]
    )
    room_number = models.CharField(
        max_length=6,
        verbose_name="Room Number",
        help_text="The room this class meets in. May contain a 1-digit building code, e.g. 250S.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['room_number'],
            message="Please enter the number of the room this class meets in, e.g. '250'. " +
                    "One letter building codes may be included, e.g. '250S'."
        )]
    )
    max_num_tas = models.PositiveIntegerField(
        default=2,
        verbose_name="Max Number of TAs",
        help_text="The maximum number of teaching assistants that can be assigned to this course, e.g. 2.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['max_num_tas'],
            message="Please enter the maximum number of TAs that can be assigned to this " +
                    "course, e.g. '3'. This field defaults to '2'."
        )]
    )
    teaching_assistants = models.ManyToManyField(
        'Profile',
        verbose_name="Teaching Assistants",
        blank=True
    )

    class Meta:
        unique_together = ('semester', 'course_number')
        ordering = ('semester', 'course_number')

    @property
    def course_number_and_name(self):
        return f'{self.course_number} - {self.name}'

    def __str__(self):
        semester = self.semester if self.semester else 'NO SEMESTER'
        return f'{semester}: {self.course_number_and_name}'


class Semester(models.Model):
    semester = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="Semester",
        help_text="A year followed by a 1-digit semester code, e.g. 2020F.",
        validators=[DataValidator(
            regex=COURSE_DATA_FORMATS['semester'],
            message="Please specify the year followed by the semester, e.g. '2020F'."
        )]
    )

    class Meta:
        ordering = ('-semester',)

    def __str__(self):
        return self.semester

    class Meta:
        ordering = ('-semester',)


class Instructor(models.Model):
    name = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Instructor",
        help_text="The name of this instructor.",
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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eagle_id = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Eagle ID",
        validators=[DataValidator(
            regex=APPILCANT_DATA_FORMATS['eagle_id'],
            message="Please enter a valid 8-digit eagle id, e.g. '58704254'."
        )]
    )
    courses_taken = models.ManyToManyField(
        Course,
        related_name="students",
        verbose_name="Courses Taken",
        blank=True
    )
    ta_assignments = models.ManyToManyField(
        Course,
        through='Course_teaching_assistants',
        verbose_name="TA Assignments",
        blank=True
    )
    lab_hour_preferences = JSONField(default=list, blank=True)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.eagle_id}: {self.full_name}'

    class Meta:
        ordering = ('user__last_name',)
        verbose_name = "Student"
        verbose_name_plural = "Students"


class SystemStatus(models.Model):
    status = models.BooleanField(default=False)
    date_changed = models.DateField(default=now)

    class Meta:
        verbose_name = "System Status"
        verbose_name_plural = "System Status"
