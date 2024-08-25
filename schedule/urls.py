from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),

    path("today", views.today, name="today"),
    path("week", views.week, name="week"),

    path("routine", views.routine, name="routine"),
    path("routine/add/<str:default_type>", views.routine_add, name="routine/add"),
    path("routine/edit/<int:routine_id>", views.routine_edit, name="routine/edit"),
    path("routine/delete/<int:routine_id>", views.routine_delete, name="routine/delete"),

    path("task", views.task, name="task"),
    path("task/add/<str:default_type>", views.task_add, name="task/add"),
    path("task/edit/<int:task_id>", views.task_edit, name="task/edit"),
    path("task/delete/<int:task_id>", views.task_delete, name="task/delete"),
    path("task/complete/<int:task_id>/<str:complete>", views.task_complete, name="task/complete"),
]