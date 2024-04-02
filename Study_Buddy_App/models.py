from django.db import models
from datetime import datetime, timedelta
from django.db.models.signals import post_migrate
from django.dispatch import receiver


# Creating the Database models
# Database model for Subjects
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Database models for Topics
class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Default deadline function to get the value of date exactly seven days from today - for initializing task model
def default_deadline():
    return datetime.today() + timedelta(days=7)


# Database model for Tasks
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    deadline = models.DateField(default=default_deadline)

    def __str__(self):
        return self.name


# Database models for Sessions
# Model for Task Session
class TaskSession(models.Model):
    DAYS_OF_WEEK = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"Task: {self.task} | Day: {self.day} | Start: {self.start_time} | End: {self.end_time}"


# Model for Topic Session
class TopicSession(models.Model):
    DAYS_OF_WEEK = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"Session for {self.topic} | Day: {self.day} | Start: {self.start_time} | End: {self.end_time}"


# Model for Submissions
class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Submission for {self.task_name} | Subject: {self.subject} | Date: {self.date}"




