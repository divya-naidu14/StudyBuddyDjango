from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from collections import defaultdict
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from datetime import date
from .models import *
from .forms import *


# Create your views here.
def home(request):
    return render(request, 'Study_Buddy_App/home.html')


# Views for the "Subjects" section
# default view to render the subjects page
def subjects(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'Study_Buddy_App/subjects.html', context)


# add_subject view to add a new subject into the database
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('subjects')


# delete the selected subject
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
    return redirect('subjects')


# Views for the "Topics and Tasks" section
# open the topics and tasks page
def topicsAndTasks(request, subject_id):
    dateToday = timezone.now().date()
    subject = Subject.objects.get(pk=subject_id)
    topics = getTopics(Topic.objects.filter(subject=subject))
    tasks = getTasks(Task.objects.filter(subject=subject, deadline__gte=dateToday))
    context = {
        'subject': subject,
        'topics': topics,
        'tasks': tasks
    }
    return render(request, 'Study_Buddy_App/topicsAndTasks.html', context)


# To add a new topic for the subject
def add_topic(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data['name']
            topic = Topic.objects.create(name=topic_name, subject=subject)
    return redirect(reverse("topics-and-tasks", kwargs={'subject_id': subject_id}))


# To delete a task from a subject
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    subject = topic.subject
    if request.method == 'POST':
        topic.delete()
    return redirect(reverse("topics-and-tasks", kwargs={'subject_id': subject.id}))


# To add a new topic for the subject
def add_task(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['name']
            task_deadline = form.cleaned_data['deadline']
            task = Task.objects.create(name=task_name, subject=subject, deadline=task_deadline)
    return redirect(reverse("topics-and-tasks", kwargs={'subject_id': subject_id}))


# Views for the "Schedule" section
# Base view that renders the schedule page
def schedule(request, date=None):
    if date is None:
        date = timezone.now().date()
        today_name = timezone.now().strftime('%A')
    else:
        if type(date) == str:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        today_name = getDayFromDate(date)
    topic_sessions = TopicSession.objects.filter(day=today_name)
    task_sessions = TaskSession.objects.filter(day=today_name, task__deadline__gte=date)
    sessions = fillSessionBlocks(getSessionBlocks(topic_sessions, task_sessions))
    formattedDate = date.strftime("%Y-%m-%d")
    context = {
        'sessions': sessions,
        'date': date,
        'formattedDate': formattedDate
    }
    return render(request, 'Study_Buddy_App/schedule.html', context)


# view to scroll to the schedule of previous day
def schedulePrevious(request, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_name = date_obj.strftime('%A')
    if day_name == "Sunday":
        previous_date = date_obj + timedelta(days=6)
    else:
        previous_date = date_obj - timedelta(days=1)

    return redirect(reverse("schedule-with-date", kwargs={'date': previous_date.strftime('%Y-%m-%d')}))


# view to scroll to the schedule of next day
def scheduleNext(request, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_name = date_obj.strftime('%A')
    if day_name == "Saturday":
        next_date = date_obj - timedelta(days=6)
    else:
        next_date = date_obj + timedelta(days=1)
    return redirect(reverse("schedule-with-date", kwargs={'date': next_date.strftime('%Y-%m-%d')}))


# add new session
def add_session(request):
    if request.method == 'POST':
        # Get form data from POST request
        subject = get_object_or_404(Subject, pk=request.POST.get('subject'))
        session_type = request.POST.get('sessionType')
        start_time = datetime.strptime(request.POST.get('startTime') + ":00", '%H:%M:%S').time()
        end_time = datetime.strptime(request.POST.get('endTime') + ":00", '%H:%M:%S').time()

        date = request.POST.get('date')
        today_name = getDayFromDate(date)
        # To check and delete if any timing intersection exists
        topic_sessions = TopicSession.objects.filter(day=today_name)
        task_sessions = TaskSession.objects.filter(day=today_name)
        session_data = {'start_time': start_time, 'end_time': end_time}
        deleteAndUpdateSessions(topic_sessions, task_sessions, session_data)

        # Determine if the session type is Topic or Task
        if session_type == 'Topic':
            # Process and save the topic session to the database
            topic = get_object_or_404(Topic, pk=request.POST.get('topic'))
            session = TopicSession.objects.create(topic=topic, start_time=start_time, end_time=end_time, day=today_name)
        elif session_type == 'Task':
            # Process and save the task session to the database
            task = get_object_or_404(Task, pk=request.POST.get('task'))
            session = TaskSession.objects.create(task=task, start_time=start_time, end_time=end_time, day=today_name)
        else:
            # Handle if neither Topic nor Task is selected
            return JsonResponse({'error': 'Invalid session type'})

        # Return a success response
        return JsonResponse({'success': True})
    else:
        # Return an error response if accessed via GET method
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# delete a task session
def delete_task_session(request, id):
    task_session = get_object_or_404(TaskSession, pk=id)
    date = request.GET.get('date', '')  # Get the date parameter from the URL
    task_session.delete()
    return redirect(reverse("schedule-with-date", kwargs={'date': date}))


# delete a topic session
def delete_topic_session(request, id):
    topic_session = get_object_or_404(TopicSession, pk=id)
    date = request.GET.get('date', '')  # Get the date parameter from the URL
    topic_session.delete()
    return redirect(reverse("schedule-with-date", kwargs={'date': date}))


# The Templates was planned feature for the project. But since it is ambiguous with the current projectscope, it is
# removed out for the time being, and is to be treated as a future project scope
def templates(request):
    return render(request, 'Study_Buddy_App/templates.html')


# Views for the Tasks section
# Base tasks view that fetches the tasks with deadline left and renders the tasks.html page
def tasks(request):
    today = date.today()
    tasks = Task.objects.filter(deadline__gte=today)
    context = {'tasks': tasks}
    return render(request, 'Study_Buddy_App/tasks.html', context)


# to delete a task
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect(reverse("tasks"))


# to mark a task as submitted
def submit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    submission = Submission.objects.create(
        task_name=task.name,
        subject=task.subject,
        date=timezone.now().date()
    )
    task.delete()
    return redirect(reverse("tasks"))


def submissions(request):
    submissions = Submission.objects.all()
    context = {'submissions': submissions}
    return render(request, 'Study_Buddy_App/submissions.html', context)


def report(request):
    today_name = date.today()
    task_sessions = TaskSession.objects.filter(task__deadline__gte=today_name)
    topic_sessions = TopicSession.objects.all()
    today = datetime.today()
    report = dict()
    for session in topic_sessions:
        topic = session.topic
        subject = topic.subject
        startTime = datetime.combine(today, session.start_time)
        endTime = datetime.combine(today, session.end_time)
        duration = endTime - startTime
        if subject not in report:
            report[subject] = {'duration': timedelta(), 'topics': dict(), 'tasks': dict()}
        subjectReport = report[subject]
        subjectReport['duration'] += duration
        topicsReport = subjectReport['topics']
        if topic not in topicsReport:
            topicsReport[topic] = {'duration': timedelta()}
        topicReport = topicsReport[topic]
        topicReport['duration'] += duration
    for session in task_sessions:
        task = session.task
        subject = task.subject
        duration = datetime.combine(today, session.end_time) - datetime.combine(today, session.start_time)
        if subject not in report:
            report[subject] = {'duration': timedelta(), 'topics': dict(), 'tasks': dict()}
        subjectReport = report[subject]
        subjectReport['duration'] += duration
        tasksReport = subjectReport['tasks']
        if task not in tasksReport:
            tasksReport[task] = {'duration': timedelta()}
        taskReport = tasksReport[task]
        taskReport['duration'] += duration

    reportContext = dict()
    for subject in report:
        subjectReport = report[subject]
        reportContext[subject] = {'duration': getDurationString(subjectReport['duration']), 'topics': dict(), 'tasks': dict()}
        topicsReport = subjectReport['topics']
        subjectReportContext = reportContext[subject]
        topicsReportContext = subjectReportContext['topics']
        for topic in topicsReport:
            topicReport = topicsReport[topic]
            topicsReportContext[topic] = {'duration': getDurationString(topicReport['duration'])}
        tasksReport = subjectReport['tasks']
        tasksReportContext = subjectReportContext['tasks']
        for task in tasksReport:
            taskReport = tasksReport[task]
            tasksReportContext[task] = {'duration': getDurationString(taskReport['duration'])}

    return render(request, 'Study_Buddy_App/report.html', {'report': reportContext})


def infoPage(request):
    return render(request, 'Study_Buddy_App/info.html')


# Utility functions
# To get the session blocks out of taskSession and topicSession Query sets,
# and store them as json/dictionary blocks along with duration
# and return them in sorted order
def getSessionBlocks(topicSessions, taskSessions):
    sessionBlocks = []
    for session in topicSessions:
        topic = session.topic
        subject = topic.subject
        start_time = session.start_time.strftime("%H:%M")
        end_time = session.end_time.strftime("%H:%M")
        duration = findDuration(start_time, end_time)
        currentBlock = {
            'id': session.id,
            'type': "Topic",
            'topic': topic.name,
            'subject': subject.name,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration
        }
        sessionBlocks.append(currentBlock)
    for session in taskSessions:
        task = session.task
        subject = task.subject
        start_time = session.start_time.strftime("%H:%M")
        end_time = session.end_time.strftime("%H:%M")
        duration = findDuration(start_time, end_time)
        currentBlock = {
            'id': session.id,
            'type': "Task",
            'task': task.name,
            'subject': subject.name,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration
        }
        sessionBlocks.append(currentBlock)
    sessionBlocks.sort(key=lambda x: x['start_time'])
    return sessionBlocks


# To find the duration between two Time Strings as an array [hrs, mins]
def findDuration(startTime, endTime):
    startTime = list(map(int, startTime.split(':')))
    endTime = list(map(int, endTime.split(':')))
    hrs = endTime[0] - startTime[0]
    mins = endTime[1] - startTime[1]
    if mins < 0:
        mins += 60
        hrs -= 1
    hrs = str(hrs).zfill(2)
    mins = str(mins).zfill(2)
    return "{}Hrs {}Mins".format(hrs, mins)


# get the duration input of format [hrs, mins] as a string of format "Hrs:Mins"
def getDurationString(duration):
    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) % 60
    return f"{hours}Hrs {minutes}Mins"


# To fill the time gaps between each consecutive sessions,
# and between start of the day and first session
# and between last session and the end of the day
def fillSessionBlocks(sessionBlocks):
    currentTime = "00:00"
    result = []
    for sessionBlock in sessionBlocks:
        if sessionBlock['start_time'] > currentTime:
            duration = findDuration(currentTime, sessionBlock['start_time'])
            result.append({
                'type': "Free",
                'start_time': currentTime,
                'end_time': sessionBlock['start_time'],
                'duration': duration
            })
        result.append(sessionBlock)
        currentTime = sessionBlock['end_time']
    if currentTime < "24:00":
        duration = findDuration(currentTime, "24:00")
        result.append({
            'type': "Free",
            'start_time': currentTime,
            'end_time': "24:00",
            'duration': duration
        })
    return result


# Sorting the task sessions day wise and time wise for the Topics and Tasks page
def getTasks(tasks):
    taskSessionObjects = []
    for task in tasks:
        taskSessions = TaskSession.objects.filter(task=task)
        currentObject = {
            'id': task.id,
            'name': task.name,
            'deadline': task.deadline
        }
        currentTaskSessions = []
        for taskSession in taskSessions:
            currentTaskSessions.append({
                'id': taskSession.id,
                'day': taskSession.day,
                'start_time': taskSession.start_time,
                'end_time': taskSession.end_time
            })
        currentTaskSessions = sortSessionsDayWise(currentTaskSessions)
        i = 1
        for session in currentTaskSessions:
            session['order'] = i
            i += 1
        currentObject['sessions'] = currentTaskSessions
        taskSessionObjects.append(currentObject)
    return taskSessionObjects


# Sorting the task sessions day wise and time wise for the Topics and Tasks page
def getTopics(topics):
    topicSessionObjects = []
    for topic in topics:
        topicSessions = TopicSession.objects.filter(topic=topic)
        currentObject = {
            'id': topic.id,
            'name': topic.name,
        }
        currentTopicSessions = []
        for topicSession in topicSessions:
            currentTopicSessions.append({
                'id': topicSession.id,
                'day': topicSession.day,
                'start_time': topicSession.start_time,
                'end_time': topicSession.end_time
            })
        currentTopicSessions = sortSessionsDayWise(currentTopicSessions)
        i = 1
        for session in currentTopicSessions:
            session['order'] = i
            i += 1
        currentObject['sessions'] = currentTopicSessions
        topicSessionObjects.append(currentObject)
    return topicSessionObjects


# To group the sessions day wise and sort them time wise
def sortSessionsDayWise(sessions):
    dayOrder = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    dayGroups = defaultdict(list)
    for session in sessions:
        dayGroups[session['day']].append(session)
    for day in dayGroups:
        dayGroups[day].sort(key=lambda x: x['start_time'])
    result = []
    for day in dayOrder:
        result.extend(dayGroups[day])
    return result


# To dynamically get subject data for the schedule page form
def get_subjects(request):
    # for python version 3.10 and above
    # if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    # For python version 3.9 and below
    # if request.method == 'GET' and request.is_ajax():
    if request.method == 'GET':
        subjects = Subject.objects.all()
        # Convert subjects queryset to JSON format
        subjects_data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return JsonResponse({'subjects': subjects_data})
    else:
        # Handle non-AJAX or invalid requests
        return JsonResponse({'error': 'Invalid request'}, status=400)


# To dynamically get data for the schedule page form
def get_topics_and_tasks(request):
    # for python version 3.10 and above
    # if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    # For python version 3.9 and below
    # if request.method == 'GET' and request.is_ajax():
    if request.method == 'GET':
        subject_id = request.GET.get('subject_id')
        date = request.GET.get('date')
        subject = get_object_or_404(Subject, pk=subject_id)
        # Assuming you have appropriate models and relationships set up
        topics = Topic.objects.filter(subject=subject)
        tasks = Task.objects.filter(subject=subject, deadline__gte=date)
        # Convert topics and tasks queryset to JSON format
        topics_data = [{'id': topic.id, 'name': topic.name} for topic in topics]
        tasks_data = [{'id': task.id, 'name': task.name} for task in tasks]
        return JsonResponse({'topics': topics_data, 'tasks': tasks_data})
    else:
        # Handle non-AJAX or invalid requests
        return JsonResponse({'error': 'Invalid request'}, status=400)


# To get the day of week from date
def getDayFromDate(date):
    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    day_of_week = date.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day_of_week]


# to erase the intersecting time sessions while adding a new session
def deleteAndUpdateSessions(topicSessions, taskSessions, sessionData):
    start = sessionData['start_time']
    end = sessionData['end_time']
    for session in topicSessions:
        if start <= session.start_time < end:
            if end < session.end_time:
                session.start_time = end
                session.save()
            else:
                session.delete()
        elif start < session.end_time <= end:
            session.end_time = start
            session.save()
    for session in taskSessions:
        if start <= session.start_time < end:
            if end < session.end_time:
                session.start_time = end
                session.save()
            else:
                session.delete()
        elif start < session.end_time <= end:
            session.end_time = start
            session.save()
