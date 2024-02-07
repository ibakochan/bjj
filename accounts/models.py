from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Jiu jitsu belt colors for each member.
    BELT_CHOICES = (
        ('White', 'White'),
        ('Blue', 'Blue'),
        ('Purple', 'Purple'),
        ('Brown', 'Brown'),
        ('Black', 'Black'),
    )

    # Member types for each member.
    MEMBER_TYPE_CHOICES = (
        ('Fivedays', 'Fivedays'),
        ('Eightdays', 'Eightdays'),
        ('Regular', 'Regular'),
    )

    # Number of stripes on the belt for each member.
    STRIPE_CHOICES = (
        (0, '0 stripes'),
        (1, '1 stripe'),
        (2, '2 stripes'),
        (3, '3 stripes'),
        (4, '4 stripes'),
    )

    # Which gym each member belongs too.
    GYM_CHOICES = (
        ('Kix', 'Kix'),
        ('Iwade', 'Iwade'),
        ('Both', 'Both'),
    )

    belt = models.CharField(max_length=20, choices=BELT_CHOICES, default='White')
    stripes = models.IntegerField(choices=STRIPE_CHOICES, default=0)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default='Regular')
    gym_choice = models.CharField(max_length=20, choices=GYM_CHOICES, default='Kix')
    date_of_birth = models.DateField(blank=True, null=True)
    # date_of_birth is currently not being used, but might be used later upon request.
    profile_picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    # profile_picture and content_type are for upploading and streaming a picture for the user.
    # I got this from dj4e django tutorials assignments"
    user_limit = models.IntegerField(default=1000)

