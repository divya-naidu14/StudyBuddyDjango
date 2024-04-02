from django.contrib import admin
from .models import *


# Admin classes to define how the data is displayed in the admin page
# Subject Model admin class
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


# Topic Model admin class
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'name')


# Task Model admin class
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'name', 'deadline')


# Task Session admin class
class TaskSessionAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'end_time', 'day')
    list_filter = ('day', )  # Add filtering by day
    search_fields = ('task', )  # Add search by task


# Topic Session admin class
class TopicSessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'start_time', 'end_time', 'day')
    list_filter = ('day',)  # Add filtering by day
    search_fields = ('topic',)  # Add search by topic


# Submissions admin class
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'subject', 'date')  # Fields to display in the list view
    list_filter = ('subject',)  # Add filters for subject
    search_fields = ('task_name',)  # Add search field for task name


# Registering the models along with their display classes
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskSession, TaskSessionAdmin)
admin.site.register(TopicSession, TopicSessionAdmin)
admin.site.register(Submission, SubmissionAdmin)
