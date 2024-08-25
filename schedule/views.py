from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    return HttpResponseRedirect(reverse("today"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "schedule/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "schedule/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "schedule/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "schedule/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "schedule/register.html")

def get_events(user, day):
    today = day
    routines = Routine.objects.filter(user=user)
    today_events = []

    for routine in routines:
        routine_days = RoutineDay.objects.filter(routine=routine)
        for routine_day in routine_days:
            if routine_day.day_of_week == today.strftime('%A'):
                event_start_time = datetime.combine(today, routine_day.start_time)
                event_end_time = datetime.combine(today, routine_day.end_time)
                
                today_events.append({
                    'title': routine.title,
                    'description': routine_day.description,
                    'start_time': event_start_time,
                    'end_time': event_end_time,
                    'color': routine.color,
                })
    
    return today_events

def get_tasks(user, day):
    today = day
    tasks = Task.objects.filter(user=user, due_date__date=today)
    return tasks

@login_required
def today(request):
    user = request.user
    hours = range(24)
    today = timezone.now().date()
    #today = today + timedelta(days=2)

    current_time = timezone.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_time_position = current_hour * 60 + current_minute
    
    events_today = get_events(user, today)
    tasks_today = get_tasks(user, today)
    
    context = {
        'hours': hours,
        'events_today': events_today,
        'tasks_today': tasks_today,
        'today': today,
        'current_time': current_time,
        'current_time_position': current_time_position,
    }

    return render(request, "schedule/today.html", context)

def get_week_days(user):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Lunes de esta semana
    days = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        days.append({
            'date': day,
            'routines': get_events(user, day),
            'tasks': get_tasks(user,day)
        })
    return days

@login_required
def week(request):
    user = request.user
    hours = range(24)
    today = timezone.now().date()

    current_time = timezone.now()
    current_date = current_time.date
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_time_position = current_hour * 60 + current_minute
    
    days = get_week_days(user)
    
    context = {
        'hours': hours,
        'days': days,
        'current_date': current_date,
        'current_time': current_time,
        'current_time_position': current_time_position
    }

    return render(request, "schedule/week.html", context)


@login_required
def routine(request):
    course_routines = Routine.objects.filter(user=request.user, type='Course')
    activity_routines = Routine.objects.filter(user=request.user, type='Activity')

    return render(request, 'schedule/routine.html', {
        'course_routines': course_routines,
        'activity_routines': activity_routines,
    })

@login_required
def routine_add(request, default_type):
    if request.method == 'POST':
        user = request.user
        type = request.POST.get('type')
        title = request.POST.get('title')
        color = request.POST.get('color')

        routine = Routine.objects.create(user=user, type=type, title=title, color=color)

        total_days = int(request.POST.get('total_days'))
        for i in range(1, total_days + 1):
            description = request.POST.get(f'description_{i}') or ''
            day_of_week = request.POST.get(f'day_of_week_{i}')
            start_time = request.POST.get(f'start_time_{i}')
            end_time = request.POST.get(f'end_time_{i}')

            RoutineDay.objects.create(
                routine=routine,
                description=description,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )

        return HttpResponseRedirect(reverse("routine"))

    return render(request, 'schedule/routine_add.html', {
        "default_type": default_type
    })

@login_required
def routine_edit(request, routine_id):

    routine = get_object_or_404(Routine, id=routine_id, user=request.user)
    
    if request.method == 'POST':
        routine.type = request.POST.get('type')
        routine.title = request.POST.get('title')
        routine.color = request.POST.get('color')
        routine.save()

        routine.days.all().delete()

        total_days = int(request.POST.get('total_days'))
        for i in range(1, total_days + 1):
            description = request.POST.get(f'description_{i}') or ''
            day_of_week = request.POST.get(f'day_of_week_{i}')
            start_time = request.POST.get(f'start_time_{i}')
            end_time = request.POST.get(f'end_time_{i}')

            RoutineDay.objects.create(
                routine=routine,
                description=description,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )

        return HttpResponseRedirect(reverse("routine"))

    return render(request, 'schedule/routine_edit.html', {
        "routine": routine,
    })


@login_required
def routine_delete(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id, user=request.user)
    routine.delete()        
    return HttpResponseRedirect(reverse("routine"))

@login_required
def task(request):
    reminder_tasks = Task.objects.filter(user=request.user, type='Reminder').order_by('due_date')
    assignment_tasks = Task.objects.filter(user=request.user, type='Assignment').order_by('due_date')
    exam_tasks = Task.objects.filter(user=request.user, type='Exam').order_by('due_date')

    completed_reminders = reminder_tasks.filter(completed=True)
    incomplete_reminders = reminder_tasks.filter(completed=False)
    
    completed_assignments = assignment_tasks.filter(completed=True)
    incomplete_assignments = assignment_tasks.filter(completed=False)
    
    completed_exams = exam_tasks.filter(completed=True)
    incomplete_exams = exam_tasks.filter(completed=False)

    now = timezone.now()

    context = {
        'incomplete_reminders': incomplete_reminders,
        'completed_reminders': completed_reminders,
        'incomplete_assignments': incomplete_assignments,
        'completed_assignments': completed_assignments,
        'incomplete_exams': incomplete_exams,
        'completed_exams': completed_exams,
        'now': now
    }

    return render(request, 'schedule/task.html', context)

@login_required
def task_add(request, default_type):
    if request.method == 'POST':

        user = request.user
        type = request.POST.get('type')
        routine_id = request.POST.get('routine') if request.POST.get('routine') != '0' else None
        title = request.POST.get('title')
        description = request.POST.get('description') or ''
        due_date = request.POST.get('due_date')

        task = Task.objects.create(user=user, type=type, routine_id=routine_id, title=title, description=description, due_date=due_date)

        return HttpResponseRedirect(reverse("task"))

    routines = Routine.objects.filter(user=request.user)
    return render(request, 'schedule/task_add.html', {
        "default_type": default_type,
        "routines": routines
    })

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    print(task)

    if request.method == 'POST':
        task.type = request.POST.get('type')
        task.routine_id = request.POST.get('routine') if request.POST.get('routine') != '0' else None
        task.title = request.POST.get('title')
        task.description = request.POST.get('description') or ''
        task.due_date = request.POST.get('due_date')
        task.save()

        return HttpResponseRedirect(reverse("task"))

    routines = Routine.objects.filter(user=request.user)

    return render(request, 'schedule/task_edit.html', {
        'task': task,
        'routines': routines
    })

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()        
    return HttpResponseRedirect(reverse("task"))

@login_required
@csrf_exempt
@require_POST
def task_complete(request, task_id, complete):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True if complete.lower() == 'true' else False
    task.save()
    return JsonResponse({
        'task_id': task.id,
        'completed': task.completed
    })
