# MediFlow Core Backend

The MediFlow core backend is a Django REST API. It is the source of truth for staff, patients, visits, and the ESI/FCFS queue. It is deliberately a core service rather than an attempt to combine the future Go queue, Flask notification, AI, and reporting services into one application.

## What is implemented

- Session login/logout compatible with the current FUTA frontend (`POST /api/login`, `POST /api/logout`).
- Role-based access: admin, doctor, nurse, reception, lab, pharmacy, and IT.
- Patient search and CRUD, using the frontend's camelCase field names.
- Departments and visits/check-ins; each visit has ESI 1–5 and is sorted by ESI then check-in time.
- Queue and dashboard summary endpoints.
- User-management, development seed data, PostgreSQL-ready Docker Compose setup, and API tests.

## Run locally

Requires Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

The API runs on `http://127.0.0.1:8000`. Serve the current frontend from the same origin through a reverse proxy, or add its development URL to `CORS_ALLOWED_ORIGINS` in `.env`. Do not use the demo accounts outside local development.

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| POST | `/api/login` | Session login: `{ "staffId", "password" }` |
| POST | `/api/logout` | End current session |
| GET | `/api/me` | Current staff member |
| GET/POST | `/api/patients` | Search (`?search=`) / register patient |
| GET/PUT/PATCH/DELETE | `/api/patients/:id` | Read or manage one patient |
| GET/POST | `/api/visits` | Check-ins and triage visits |
| GET | `/api/queue?department=opd` | Waiting patients, ESI then FCFS |
| GET | `/api/dashboard` | Daily operational counts |
| GET/POST | `/api/users` | Admin-only staff management |

Run the verification suite with `python manage.py test`.

## Security notes

Set a strong `DJANGO_SECRET_KEY`, turn `DJANGO_DEBUG=false`, use HTTPS, and restrict `DJANGO_ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` before deployment. This starter is not a substitute for clinical validation, a privacy impact assessment, encrypted backups, monitoring, or compliance controls.
