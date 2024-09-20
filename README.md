# Uniagenda: University Task Manager

## Project Overview

Uniagenda is a web application designed to help university students manage their tasks, schedules, and activities efficiently. The application includes features for viewing and managing today’s activities, weekly schedules, courses, tasks, exams, recurring activities, and reminders. It leverages Django for the backend and JavaScript for interactive front-end functionalities, ensuring a robust and responsive user experience.

## Features

- **Today**: View a detailed calendar to track all activities and tasks scheduled for the current day.
- **Week**: Check a overview of scheduled activities and tasks planned throughout the week.
- **Routine**: Manage courses and recurring activities with the ability to add, delete, or modify them on a weekly basis.
- **Tasks**: Create and organize assignments, exams, and reminders by assigning due dates and associating them with specific courses or activities.

## File Structure

- `manage.py`: Django management script.
- `README.md`: Project documentation.
- `db.sqlite`: Database in sqlite3.
- `uniagenda/`: Project directory containing settings and configurations.
- `schedule/`: Django app for managing routines and tasks.
  - `models.py`: Defines the data models for users, routines, routine days and tasks.
  - `urls.py`: URL routing for the app, including user authentication, today and week urls, routine management and task management.
  - `views.py`: Contains view functions for rendering task-related pages. User authentication with login, registration and logout views and logic. The today and week functions obtain the routine, tasks and time related information to show in the view. Routine management allows showing the users courses and activities, a routine creation view, edition view and delete logic. Task management allows same things presenting, creating, editing and deleting assignments, exams and reminders.
  - `templates/schedule/`: HTML templates for layout, login, register, today, week, routine management and task management.
  - `static/schedule/`: Logo and CSS files for frontend styling.
  - `migrations/`: Database migrations created by Django.

## Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/uniagenda.git
   cd uniagenda
   ```
2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Run the server
   ```bash
   python manage.py runserver
   ```
4. Open your browser and navigate to http://127.0.0.1:8000 to use the application.
