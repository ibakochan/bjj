from django.urls import path, reverse_lazy
from . import views




app_name='main'
urlpatterns = [
    path('profile/<int:user_id>/', views.ProfilePageView.as_view(), name='profile'),
    path('iwade_lesson/list', views.LessonListView.as_view(), name='lesson_list'),
    path('profile/picture/<int:user_id>/', views.profile_stream_file, name='profile_picture'),
    path('button/<int:pk>/', views.ButtonPageView.as_view(), name='button_page'),
    path('button/<int:pk>/delete/<int:lesson_pk>/', views.ButtonDeleteView.as_view(success_url=reverse_lazy('main:button_page')), name='button_delete'),
    path('lesson/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/picture/<int:pk>/', views.stream_file, name='lesson_picture'),
    path('lesson/<int:pk>/delete', views.LessonDeleteView.as_view(success_url=reverse_lazy('main:lesson_list')), name='lesson_delete'),
    path('participation_increase/<int:pk>/<int:click_id>/', views.ParticipationIncreaseView.as_view(), name='participation_increase'),
    path('delete/<int:pk>/', views.AccountDeleteView.as_view(), name='delete_account'),
    path('', views.BjjLessonListView.as_view(), name='bjj_lesson_list'),
    path('set-user-limit/', views.SetUserLimitView.as_view(), name='set_user_limit'),
    path('reset_monthly_counts/', views.ResetMonthlyCountsView.as_view(), name='reset_monthly_counts'),
    path('profile/<int:user_id>/participation_count/', views.ParticipationCountView.as_view(), name='participation_count'),
    path('add_users_to_lessons/', views.AddUsersToLessonsView.as_view(), name='add_users_to_lessons'),
]

