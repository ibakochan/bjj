from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class Lesson(models.Model) :
    title = models.CharField(
            max_length=200,
    )

    # To decide which day in the schedule the lesson will be place in.
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    # To decide in which order from top to bottom of the scheule the lesson will be placed.
    SPOT_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]


    # The purpose of categories was originally to have a seperate count for each lesson category.
    # Still left this here as it can be nice to know the type of lesson anyways.
    CATEGORY_CHOICES = [
        ('Jiu Jitsu', 'Jiu Jitsu'),
        ('Free Mat', 'Free Mat'),
        ('Competition', 'Competition'),
        ('Basic', 'Basic'),
    ]

    # Color for the lesson title in the schedule.
    COLOR_CHOICES = [
        ('sky', 'Sky'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('light red', 'Light Red'),
    ]

    # The owner got 2 gyms, so i made 2 seperate schedules.
    SCHOOL_CHOICES = [
        ('Kix', 'Kix'),
        ('Iwade', 'Iwade'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True)
    spot = models.IntegerField(choices=SPOT_CHOICES, null=True)
    text = models.TextField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
    time = models.CharField(max_length=12, null=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, null=True)

class ParticipationCount(models.Model):
    # Taking monthly jiu jitsu participation counts and counts for each belt color.

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)

    monthly_count_j = models.PositiveIntegerField(default=0)

    white_jiu_jitsu_count = models.PositiveIntegerField(default=0)
    blue_jiu_jitsu_count = models.PositiveIntegerField(default=0)
    purple_jiu_jitsu_count = models.PositiveIntegerField(default=0)
    brown_jiu_jitsu_count = models.PositiveIntegerField(default=0)
    black_jiu_jitsu_count = models.PositiveIntegerField(default=0)




class Click(models.Model):
    # For putting members names into the lesson to increase their participationcounts later.

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)