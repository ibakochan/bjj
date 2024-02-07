from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from main.models import Click, Lesson, ParticipationCount
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from accounts.models import CustomUser
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers





from main.forms import CreateForm, UserPreferencesForm, ParticipationCountForm
from django.contrib.auth.mixins import LoginRequiredMixin
from main.owner import OwnerDeleteView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse





class SetUserLimitView(View):
    # For setting a limit to the number of members allowed.
    # This is being used with a middle ware that prevents access to the signup page if the limit is reached.
    template_name = 'main/profile.html'

    def post(self, request, *args, **kwargs):
        user_limit = request.POST.get('user_limit')
        current_user = self.request.user
        current_user.user_limit = int(user_limit)
        current_user.save()
        return redirect('main:profile', user_id=current_user.id)




class ProfilePageView(View):
    # View for displaying details of a member.
    # Includes various things like profile pic, belt color, participation counts etc.

    model = CustomUser
    template_name = 'main/profile.html'


    def get(self, request, user_id):
        # Gets the current belt, gym etc for the UserPreferencesForm.
        # And gets the current participation counts for the user as initial input in the form.
        user = get_object_or_404(CustomUser, id=user_id)
        users = CustomUser.objects.all()

        user_preferences_form = UserPreferencesForm(instance=user)

        participation_counts = ParticipationCount.objects.filter(user=user)

        total_white_count = sum(pc.white_jiu_jitsu_count for pc in participation_counts)
        total_blue_count = sum(pc.blue_jiu_jitsu_count for pc in participation_counts)
        total_purple_count = sum(pc.purple_jiu_jitsu_count for pc in participation_counts)
        total_brown_count = sum(pc.brown_jiu_jitsu_count for pc in participation_counts)
        total_black_count = sum(pc.black_jiu_jitsu_count for pc in participation_counts)


        participation_count_form = ParticipationCountForm(
            initial={
                'user': user,
                'white_jiu_jitsu_count': total_white_count,
                'blue_jiu_jitsu_count': total_blue_count,
                'purple_jiu_jitsu_count': total_purple_count,
                'brown_jiu_jitsu_count': total_brown_count,
                'black_jiu_jitsu_count': total_black_count,
            }
        )

        return render(request, self.template_name, {'user': user, 'users': users, 'user_preferences_form': user_preferences_form, 'participation_count_form': participation_count_form})

    def get_context_data(self, **kwargs):
        # To get the user of the current profile page.
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']

        user_id = int(user_id)

        context['user_id'] = user_id
        return context

    def post(self, request, user_id):
        # For changing information about the user using the form.

        user = get_object_or_404(CustomUser, id=user_id)
        users = CustomUser.objects.all()

        user_preferences_form = UserPreferencesForm(request.POST, request.FILES or None, instance=user)

        if user_preferences_form.is_valid():
            user_preferences_form.save()


            return redirect('main:profile', user_id=user.id)
        else:
            return render(request, self.template_name, {
                'user': user,
                'users': users,
                'user_preferences_form': user_preferences_form,
            })



def profile_stream_file(request, user_id):
    # This is got from the dj4e tutorial.
    # Lets you stream the picture in a different url and so I can use that link to display it on a page.

    user = get_object_or_404(CustomUser, id=user_id)
    response = HttpResponse()
    response['Content-Type'] = user.content_type
    response['Content-Length'] = len(user.profile_picture)
    response.write(user.profile_picture)
    return response



class ParticipationCountView(View):
    # Lets you change the participation count of a user manually using the form.

    template_name = 'main/profile.html'

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        ParticipationCount.objects.filter(user=user).delete()
        participation_count = ParticipationCount.objects.create(user=user)

        form = ParticipationCountForm(request.POST, instance=participation_count)

        if form.is_valid():


            participation_count.save()

            success_url = reverse('main:profile', kwargs={'user_id': participation_count.user.id})
            return redirect(success_url)
        else:
            return render(request, self.template_name, {'user': user, 'form': form, 'participation_count': participation_count})






class AddUsersToLessonsView(View):
    # Lets you add each member to all lessons of each respective school.

    template_name = 'main/bjj_lesson_list.html'

    def post(self, request, *args, **kwargs):
        kix_users = CustomUser.objects.filter(gym_choice='Kix')
        iwade_users = CustomUser.objects.filter(gym_choice='Iwade')
        both_users = CustomUser.objects.filter(gym_choice='Both')

        kix_lessons = Lesson.objects.filter(school='Kix')
        iwade_lessons = Lesson.objects.filter(school='Iwade')

        for user in kix_users:
            for lesson in kix_lessons:
                Click.objects.get_or_create(user=user, lesson=lesson)

        for user in iwade_users:
            for lesson in iwade_lessons:
                Click.objects.get_or_create(user=user, lesson=lesson)

        for user in both_users:
            for lesson in kix_lessons:
                Click.objects.get_or_create(user=user, lesson=lesson)

            for lesson in iwade_lessons:
                Click.objects.get_or_create(user=user, lesson=lesson)

        return HttpResponseRedirect(reverse('main:bjj_lesson_list'))



class ResetMonthlyCountsView(View):
    # Lets you reset all monthly jiu jitsu counts for all users.

    def get(self, request):
        all_users = CustomUser.objects.all()
        for user in all_users:
            participation_counts = ParticipationCount.objects.filter(user=user)
            for count in participation_counts:
                count.monthly_count_j = 0
                count.save()

        return HttpResponseRedirect(reverse('main:lesson_list'))





class AccountDeleteView(OwnerDeleteView):
    # Using the OwnerDeleteView I got from dj4e to delete accounts.

    model = CustomUser
    template_name = 'main/profile.html'

    def get_success_url(self):
        current_user_id = self.request.user.id
        return reverse('main:profile', kwargs={'user_id': current_user_id})


class LessonListView(View):
    # For displaying Iwade lessons on the page.

    model = Lesson
    template_name = "main/lesson_list.html"

    def get(self, request) :
        lesson_list = Lesson.objects.all()
        school = 'Iwade'
        day_choices = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        spots = range(1, 6)

        ctx = {
            'lesson_list' : lesson_list,
            'school': school,
            'day_choices': day_choices,
            'spots': spots,
        }
        return render(request, self.template_name, ctx)

class BjjLessonListView(View):
    # For displaying Kix lessons on the page.

    model = Lesson
    template_name = "main/bjj_lesson_list.html"

    def get(self, request) :
        lesson_list = Lesson.objects.all()
        school = 'Kix'
        day_choices = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        spots = range(1, 6)

        ctx = {
            'lesson_list' : lesson_list,
            'school': school,
            'day_choices': day_choices,
            'spots': spots,
        }
        return render(request, self.template_name, ctx)




class LessonCreateView(LoginRequiredMixin, View):
    # View for creating a lesson using the Createform.

    template_name = 'main/lesson_form.html'

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        if form.is_valid():
            day = form.cleaned_data['day']
            spot = form.cleaned_data['spot']
            school = form.cleaned_data['school']
            lesson_spot_used = Lesson.objects.filter(day=day, spot=spot, school=school).exists()

            if not lesson_spot_used:
                lesson = form.save(commit=False)
                lesson.owner = self.request.user
                lesson.save()
                if school == 'Iwade':
                    return redirect('main:lesson_list')
                elif school == 'Kix':
                    return redirect('main:bjj_lesson_list')
                else:
                    return redirect('main:lesson_list')
            else:
                ctx = {'form': form, 'error_message': 'This day and spot already exist.'}
                return render(request, self.template_name, ctx)
        else:
            ctx = {'form': form}
            return render(request, self.template_name, ctx)



class LessonUpdateView(LoginRequiredMixin, View):

    template_name = 'main/lesson_update.html'

    def get(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        form = CreateForm(instance=lesson)
        ctx = {'form': form, 'lesson': lesson}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        form = CreateForm(request.POST, request.FILES or None, instance=lesson)

        if not form.is_valid():
            ctx = {'form': form, 'lesson': lesson}
            return render(request, self.template_name, ctx)

        if form.is_valid():
            day = form.cleaned_data['day']
            spot = form.cleaned_data['spot']
            school = form.cleaned_data['school']
            lesson_spot_used = Lesson.objects.filter(day=day, spot=spot, school=school).exclude(pk=pk).exists()

            if not lesson_spot_used:
                lesson = form.save(commit=False)
                lesson.owner = self.request.user
                lesson.save()
                if lesson.school == 'Iwade':
                    return redirect('main:lesson_list')
                elif lesson.school == 'Kix':
                    return redirect('main:bjj_lesson_list')
                else:
                    return redirect('main:lesson_list')
            else:
                ctx = {'form': form, 'lesson': lesson, 'error_message': 'This day and spot already exist.'}
                return render(request, self.template_name, ctx)
        else:
            ctx = {'form': form, 'lesson': lesson}
            return render(request, self.template_name, ctx)



def stream_file(request, pk):
    # same kind of picture stream as the one used for profile pics.

    lesson = get_object_or_404(Lesson, id=pk)
    response = HttpResponse()
    response['Content-Type'] = lesson.content_type
    response['Content-Length'] = len(lesson.picture)
    response.write(lesson.picture)
    return response


class ButtonPageView(LoginRequiredMixin, View):
    # Lets you add a member to a lesson.

    template_name = 'main/button_page.html'
    model = Click

    def get(self, request, pk):

        lesson = Lesson.objects.get(pk=pk)
        clicks = Click.objects.filter(lesson=lesson)
        limit = len(clicks) <= 9
        total_capacity = 10
        spots_open = total_capacity - len(clicks)
        return render(request, 'main/button_page.html', {
            'clicks': clicks,
            'limit': limit,
            'spots_open': spots_open,
            'lesson': lesson,
        })

    def post(self, request, pk):
        if request.method == 'POST':
          user = request.user
          lesson = get_object_or_404(Lesson, pk=pk)

        if not Click.objects.filter(user=user, lesson=lesson).exists():
            click = Click.objects.create(user=user, lesson=lesson)
            click.save()

        return HttpResponseRedirect(reverse('main:button_page', args=[pk]))


class ParticipationIncreaseView(LoginRequiredMixin, View):
    # Lets you increase a members participation count for monthly count and its current belt color.
    # I made it a jsonresponse to use ajax to not refresh the page after each increase.
    # I added serialize and timestamp to be able to order member from most recent participants.

    def post(self, request, pk, click_id):
        lesson = Lesson.objects.get(pk=pk)
        click = Click.objects.get(pk=click_id, lesson=lesson)
        user = click.user

        participation_count, created = ParticipationCount.objects.get_or_create(
            user=user,
            lesson=lesson
        )

        participation_count.monthly_count_j += 1

        if user.belt == 'White':
            participation_count.white_jiu_jitsu_count += 1
        elif user.belt == 'Blue':
            participation_count.blue_jiu_jitsu_count += 1
        elif user.belt == 'Purple':
            participation_count.purple_jiu_jitsu_count += 1
        elif user.belt == 'Brown':
            participation_count.brown_jiu_jitsu_count += 1
        elif user.belt == 'Black':
            participation_count.black_jiu_jitsu_count += 1


        participation_count.save()

        click.order = timezone.now()
        click.timestamp = timezone.now()
        click.save()

        clicks = Click.objects.filter(lesson=lesson, user=user).order_by('-order')

        clicks_json = serializers.serialize('json', clicks)


        response_data = {
            'user_id': user.id,
            'click_id': click.id,
            'timestamp': click.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_counts': {
                'monthly_count_j':  participation_count.monthly_count_j,
                'white_jiu_jitsu_count': participation_count.white_jiu_jitsu_count,
                'blue_jiu_jitsu_count': participation_count.blue_jiu_jitsu_count,
                'purple_jiu_jitsu_count': participation_count.purple_jiu_jitsu_count,
                'brown_jiu_jitsu_count': participation_count.brown_jiu_jitsu_count,
                'black_jiu_jitsu_count': participation_count.black_jiu_jitsu_count,
            },
            'clicks': clicks_json,
        }

        return JsonResponse(response_data)


class ButtonDeleteView(OwnerDeleteView):
    # Lets you delete a user from a certain lesson if they never participate on it.
    model = Click
    template_name = 'main/button_page.html'

    def get_success_url(self):
        lesson_pk = self.kwargs['lesson_pk']
        return reverse_lazy('main:button_page', kwargs={'pk': lesson_pk})




class LessonDeleteView(OwnerDeleteView):
    # Lets you delete a lesson.
    # Deleting a lesson does not affect any participation counts associated with the lesson.

    model = Lesson
    template_name = 'main/button_page.html'

    def get_success_url(self):
        lesson = self.get_object()
        if lesson.school == 'Iwade':
            return reverse('main:lesson_list')
        elif lesson.school == 'Kix':
            return reverse('main:bjj_lesson_list')
        else:
            return reverse('main:lesson_list')

