# EngageIU — Campus Event Attendance Leaderboard

Built for the **Luddy Hacks 24-Hour Hackathon** — Dynamic Leaderboard/Ranking System case (Graduate Team).

Students earn points by entering event check-in codes. The leaderboard ranks participants by total weekly points. Admins manage events, students, and entries through a protected panel.

---

## Architecture

```
Browser (HTML/CSS/JS)
        │
        │  HTTP (REST)
        ▼
┌─────────────────────────────────┐
│  FastAPI (Python 3.11)          │
│  ├─ /add  /remove  /leaderboard │  ← required by case PDF
│  ├─ /info  /performance         │  ← required by case PDF
│  ├─ /history                    │  ← grad-team requirement
│  ├─ /events  /checkin           │  ← EngageIU-specific
│  └─ /auth/login (JWT)           │
│                                 │
│  Performance Middleware         │  ← auto-logs every request
│  StaticFiles → frontend/        │  ← serves HTML/CSS/JS
└────────────┬────────────────────┘
             │  SQLAlchemy ORM
             ▼
      SQLite (engageiu.db)
      ├─ students
      ├─ events
      ├─ attendance
      └─ endpoint_performance
```

---

## Setup

### Option A: Docker (recommended)

```bash
git clone <repo-url>
cd engageiu
docker-compose up --build
```

- API + frontend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Admin panel: http://localhost:8000/static/admin.html

### Option B: Without Docker

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> The frontend is served by FastAPI. No separate server needed.

**Default admin credentials:**
- Username: `admin`
- Password: `engageiu2025`

Override with env vars: `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `SECRET_KEY`

---

## API Documentation

Swagger UI (interactive): http://localhost:8000/docs

OpenAPI YAML spec: `openapi.yaml` in the project root — import directly into [Swagger Editor](https://editor.swagger.io/).

---

## Endpoint Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/login | — | Admin login, returns JWT |
| **POST** | **/add** | Admin | Add a leaderboard entry |
| **DELETE** | **/remove** | Admin | Remove a leaderboard entry |
| **GET** | **/leaderboard** | Public | Top 10 weekly leaderboard (`?format=html` for table) |
| **GET** | **/info** | Public/Admin | Score statistics (extended stats for admin) |
| **GET** | **/performance** | Admin | Average endpoint execution times |
| **GET** | **/history** | Admin | Score submission log with date/user filtering |
| GET | /events | Public/Admin | List events (admin sees check-in codes) |
| POST | /events | Admin | Create event (auto-generates code) |
| PATCH | /events/{id} | Admin | Update event or regenerate code |
| DELETE | /events/{id} | Admin | Delete event |
| GET | /events/{id}/code | Admin | Get check-in code for event |
| POST | /checkin | Public | Student self check-in |
| GET | /students/search | Public | Search students by name or username |

---

## Student Check-In Flow

1. Student attends a real IU event
2. Admin shares the event's check-in code (from admin panel or events page)
3. Student visits **EngageIU** → clicks **Check In**
4. Enters: Full Name, IU Username, Campus, Event Code
5. System validates code, records attendance, returns rank + points
6. Leaderboard updates automatically (auto-refreshes every 30 seconds)

---

## Admin Guide

1. Navigate to http://localhost:8000/static/admin.html
2. Login with admin credentials
3. **Leaderboard tab**: view this week's rankings, add/remove entries
4. **Statistics tab**: view all score stats (mean, median, Q1/Q3, std dev, distribution, percentile ranks)
5. **Performance tab**: monitor endpoint response times
6. **History tab**: filter submission log by date range or username
7. On the **Events page**: admin controls appear on each event card (edit, delete, copy code, regenerate code)

---

## Graduate Requirements Checklist

- [x] **Docker containerization** — `Dockerfile` + `docker-compose.yml` provided
- [x] **`/history` with filtering** — supports `start_date`, `end_date`, `iu_username` query params; paginated; sorted newest first
- [x] **`/info` extended stats** — std_deviation, percentile_ranks (array), score_distribution (bucketed histogram), top_campus, most_attended_event, weekly_growth_rate_pct
- [x] **OpenAPI YAML** — `openapi.yaml` in project root, covers all required endpoints (/add, /remove, /leaderboard, /info) plus all others
- [x] **Performance middleware** — auto-records every request to `endpoint_performance` table; no manual logging needed

---

## Technical Notes

- All statistics (mean, median, Q1/Q3, std dev, percentile ranks, score distribution) are implemented in **pure Python** in `backend/utils/stats.py` — no external statistics libraries
- Frontend uses **plain HTML, CSS, and vanilla JavaScript** — no frameworks, no CSS libraries
- The `/leaderboard` SQL query uses **`GROUP BY` + `SUM` at the database level** — no Python-side aggregation
- Check-in codes generated with Python's **`secrets` module** (cryptographically secure), 8 characters, alphanumeric uppercase
- Attendance records are **immutable once inserted** — admins can remove them but not edit them
- All timestamps stored and returned as **ISO 8601 UTC**; frontend converts to local time
