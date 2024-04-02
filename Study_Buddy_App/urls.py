from django.urls import path
from . import views


urlpatterns = [
    # base url
    path('', views.home, name='home'),

    # urls for subjects page
    path('subjects', views.subjects, name='subjects'),
    path('add-subject/', views.add_subject, name='add-subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete-subject/'),

    # urls for topics and tasks page
    path('topics-and-tasks/<int:subject_id>/', views.topicsAndTasks, name='topics-and-tasks'),
    path('add-topic/<int:subject_id>/', views.add_topic, name='add-topic'),
    path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('add-task/<int:subject_id>/', views.add_task, name='add-task'),

    # urls for schedule page
    path('schedule', views.schedule, name='schedule'),
    path('schedule/<str:date>/', views.schedule, name='schedule-with-date'),
    path('schedule-previous/<str:date>/', views.schedulePrevious, name='schedule-previous'),
    path('schedule-next/<str:date>/', views.scheduleNext, name='schedule-next'),
    # the following urls are to get data dynamically for the form
    path('get-topics-and-tasks/', views.get_topics_and_tasks, name='get-topics-and-tasks'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    # the following urls are for addition and deletion of sessions
    path('add-session/', views.add_session, name='add-session'),
    path('delete-task-session/<int:id>/', views.delete_task_session, name='delete-task-session'),
    path('delete-topic-session/<int:id>/', views.delete_topic_session, name='delete-topic-session'),

    # urls for templates page
    path('templates', views.templates, name='templates'),

    # urls for tasks page
    path('tasks', views.tasks, name='tasks'),
    path('delete-task/<int:id>/', views.delete_task, name='delete-task'),
    path('submit-task/<int:id>/', views.submit_task, name='submit-task'),

    path('submissions', views.submissions, name='submissions'),
    path('report', views.report, name='report'),
    path('help', views.helpPage, name='help'),
    # path('time_tracker', views.timeBlocks, name='time-blocks'),
    # path('delete_time_block/<int:pk>', views.deleteTimeBlock, name='delete-time-block'),
    # path('help', views.help, name='help')
]

