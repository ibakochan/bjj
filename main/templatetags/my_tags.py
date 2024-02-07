from django import template
from main.models import Lesson, Click, ParticipationCount
from django.urls import reverse
from accounts.models import CustomUser



register = template.Library()


@register.simple_tag
def total_jiu_jitsu_participation_count(user):
    # For displaying the total amount of lessons a user has participated in over all time.

    participation_counts = ParticipationCount.objects.filter(user=user)

    total_count = sum(
        count.white_jiu_jitsu_count +
        count.blue_jiu_jitsu_count +
        count.purple_jiu_jitsu_count +
        count.brown_jiu_jitsu_count +
        count.black_jiu_jitsu_count
        for count in participation_counts
    )

    return total_count

# All these 5 tags displays the number of participations for each belt color.
@register.simple_tag
def white_jiu_jitsu_participation_count(user):
    participation_counts = ParticipationCount.objects.filter(user=user)
    return sum(count.white_jiu_jitsu_count for count in participation_counts)

@register.simple_tag
def blue_jiu_jitsu_participation_count(user):
    participation_counts = ParticipationCount.objects.filter(user=user)
    return sum(count.blue_jiu_jitsu_count for count in participation_counts)

@register.simple_tag
def purple_jiu_jitsu_participation_count(user):
    participation_counts = ParticipationCount.objects.filter(user=user)
    return sum(count.purple_jiu_jitsu_count for count in participation_counts)

@register.simple_tag
def brown_jiu_jitsu_participation_count(user):
    participation_counts = ParticipationCount.objects.filter(user=user)
    return sum(count.brown_jiu_jitsu_count for count in participation_counts)

@register.simple_tag
def black_jiu_jitsu_participation_count(user):
    participation_counts = ParticipationCount.objects.filter(user=user)
    return sum(count.black_jiu_jitsu_count for count in participation_counts)


@register.simple_tag(takes_context=True)
def user_limit(context):
    # Gets you the limit for number of members.

    request = context['request']
    if request.user.is_authenticated:
        user_limit = CustomUser.objects.get(id=request.user.id).user_limit
        return user_limit
    return 0

@register.simple_tag
def get_customuser_count():
    # Gets you the number of members.

    return CustomUser.objects.count()



@register.simple_tag
def jiu_jitsu_monthly_count(user):
    # Gets you the monthly participation counts for members.

    participation_counts = ParticipationCount.objects.filter(user=user)
    total_jiu_jitsu_monthly_count = sum(count.monthly_count_j for count in participation_counts)
    return total_jiu_jitsu_monthly_count


# The following 4 tags displays a message when its time to give a new stripe to a member.
@register.simple_tag
def white_jiu_jitsu_message(user_id):
    participations = ParticipationCount.objects.filter(user_id=user_id)

    if participations.exists():
        total_count = sum(participation.white_jiu_jitsu_count for participation in participations)

        if total_count in [10, 11, 12, 13, 14, 40, 41, 42, 43, 44, 70, 71, 72, 73, 74, 100, 101, 102, 103, 104]:
            return 'Time for a new stripe!'

    return ''


@register.simple_tag
def blue_jiu_jitsu_message(user_id):
    participations = ParticipationCount.objects.filter(user_id=user_id)

    if participations.exists():
        total_count = sum(participation.blue_jiu_jitsu_count for participation in participations)

        if total_count in [60, 61, 62, 63, 64, 120, 121, 122, 123, 124, 180, 181, 182, 183, 184, 240, 241, 242, 243, 244]:
            return 'Time for a new stripe!'

    return ''

@register.simple_tag
def purple_jiu_jitsu_message(user_id):
    participations = ParticipationCount.objects.filter(user_id=user_id)

    if participations.exists():
        total_count = sum(participation.purple_jiu_jitsu_count for participation in participations)

        if total_count in [50, 51, 52, 53, 54, 100, 101, 102, 103, 104, 150, 151, 152, 153, 154, 200, 201, 202, 203, 204]:
            return 'Time for a new stripe!'

    return ''

@register.simple_tag
def brown_jiu_jitsu_message(user_id):
    participations = ParticipationCount.objects.filter(user_id=user_id)

    if participations.exists():
        total_count = sum(participation.brown_jiu_jitsu_count for participation in participations)

        if total_count in [55, 56, 57, 58, 59, 110, 111, 112, 113, 114, 165, 166, 167, 168, 169, 220, 221, 222, 223, 224]:
            return 'Time for a new stripe!'

    return ''


@register.filter(name='sort_by_day_order')
def sort_by_day_order(value):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return sorted(value, key=lambda lesson: day_order.index(lesson.day))
