# Schoolcore

Schoolcore is a Django-based school management application designed to manage core academic and administrative operations such as student records, teacher records, attendance, assessments, finance, and reporting.

This project is organized as a modular Django monolith, with each domain separated into its own app package.

## Project overview

The application exposes a dashboard and separate modules for key school workflows:

- Student registration and enrolment
- Teacher management
- Academic structures such as classes and subjects
- Attendance tracking
- Assessments
- Finance and fee allocation
- Reporting
- Authentication and dashboard access

## Tech stack

- Python
- Django 6.1
- PostgreSQL support via `dj-database-url`
- SQLite default for local development
- WhiteNoise for static files
- Django admin and templates

## Repository structure

```text
schoolcore/
├── academics/            # Academic structures such as classes, sections, subjects, years
├── accounts/             # Authentication and user account flow
├── assessments/         # Assessment-related views and logic
├── attendance/           # Attendance tracking
├── config/               # Django settings, routing, ASGI/WSGI setup
├── dashboard/            # Home/dashboard views and summary widgets
├── finance/              # Finance logic, fee allocation, billing-related logic
├── reports/              # Reporting interfaces
├── students/             # Student profiles, guardians, and enrolment records
├── teachers/             # Teacher records and related logic
├── templates/            # Shared templates
├── .env.example          # Example environment file
├── .gitignore
├── build.sh
├── manage.py
├── requirements.txt
└── db.sqlite3            # local SQLite database (generated in development)
```

## Key application entry points

### `manage.py`

This is the standard Django project entry point. It is used to run migrations, start the development server, and execute management commands.

### `config/settings.py`

This file contains the main Django configuration:

- Installed apps
- Secret key and environment settings
- Debug mode and host configuration
- Database configuration
- Templates configuration
- Static files configuration
- Custom auth model
- Security settings for deployment

Important settings include:

- `AUTH_USER_MODEL = "accounts.User"`
- `LOGIN_REDIRECT_URL = "/dashboard/"`
- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- production security settings are enabled when `DEBUG` is false

### `config/urls.py`

This is the project-level URL router. It maps the root path and routes traffic into the app-specific URL files:

- `/` redirects to the dashboard
- `/admin/`
- `/dashboard/`
- `/students/`
- `/finance/`
- `/teachers/`
- `/accounts/`
- `/assessments/`
- `/attendance/`
- `/academics/`
- `/reports/`

## App-level documentation

### `accounts`

Responsible for authentication and user session management. The project uses Django's built-in auth views:

- `login/`
- `logout/`

The default login page is served from `templates/accounts/login.html` and redirects to the dashboard after a successful login.

### `dashboard`

Handles the main dashboard landing page. The `dashboard_home` view collects summary counts such as:

- active students
- active teachers
- class count
- subject count
- attendance count

This is a high-level overview for school administrators.

### `students`

The student module defines core student-domain models, including:

- `Student`
- `Guardian`
- `Enrolment`

Important business logic:

- `Student` stores student profile information such as name, DOB, gender, contact data, and active status.
- `Guardian` stores parent or guardian information linked to a student.
- `Enrolment` links a student to an academic year and section.
- Each new enrolment triggers fee allocation through `allocate_fees_for_enrolment` from `finance.services`.

Routes include:

- `""` -> list students
- `"<int:student_id>/"` -> student detail
- `"new/"` -> create student

### `teachers`

The teacher module is expected to manage teacher profiles and teacher-related academic assignments. The application structure indicates a dedicated teacher domain, likely separate from the student domain.

### `academics`

Responsible for academic structure, such as:

- school classes
- sections
- academic years
- subjects

This module likely defines the school’s academic organization and supports links from student enrolments and teacher assignments.

### `attendance`

Tracks attendance records for students or school activities. It is one of the core operational modules and is referenced in the dashboard summary view.

### `assessments`

Handles student assessments, grades, and evaluation workflows. It is included as a top-level application in the Django project settings and URLs.

### `reports`

Provides reporting views for school data, likely summarizing attendance, academic performance, and institutional statistics.

### `finance`

Handles finance-related logic. The student enrolment model explicitly calls into `finance.services.allocate_fees_for_enrolment`, which suggests fee generation or financial record setup is automated when a student is enrolled.

### `config`

Contains the project-level infrastructure code:

- `settings.py`
- `urls.py`
- `asgi.py`
- `wsgi.py`

These define the runtime environment and how Django initializes the application.

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

The project supports environment-based configuration via environment variables such as:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- database URL settings if used in production

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Start the app

```bash
python manage.py runserver
```

## Local development notes

- The default database is SQLite unless a database URL is provided.
- `DEBUG` is enabled by default from the environment, which is useful during development.
- The project is configured for deployment on Render, as indicated by the host configuration and security settings.

## Security considerations

- Do not use the fallback development secret key in production.
- Set a proper `SECRET_KEY` in production.
- Restrict `ALLOWED_HOSTS` to approved deployment domains.
- Configure secure HTTPS settings when deploying externally.
- Keep environment variables out of source control.

## Future documentation recommendations

To improve maintainability, the project would benefit from:

- a dedicated `README` for each app module
- API endpoint documentation
- database schema documentation
- business rule documentation for fees, attendance, and assessments
- contributor setup instructions for local workflows

## Summary

Schoolcore is a Django-based school administration system structured around domain-specific apps. The main strengths are its modular architecture, clear separation of responsibilities, and built-in Django conventions. The codebase is organized enough to extend and maintain, with a strong foundation for student, academic, and administrative workflows.

This README provides a practical high-level overview of the project structure and the responsibilities of each major module.
