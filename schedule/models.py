from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    type = models.CharField(max_length=8, choices=[
        ('Course', 'Course'),
        ('Activity', 'Activity')
    ])
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

class RoutineDay(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='days')
    description = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

'''
class Event():
    routine_day = models.ForeignKey(RoutineDay, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
'''
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    type = models.CharField(max_length=10, choices=[
        ('Reminder', 'Reminder'),
        ('Assignment', 'Assignment'),
        ('Exam', 'Exam')
    ])
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='tasks', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
