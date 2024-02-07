from django.contrib import admin
from main.models import Click, Lesson, ParticipationCount

admin.site.register([Click, Lesson, ParticipationCount])
