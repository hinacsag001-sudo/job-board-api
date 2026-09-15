# Job Listings REST API

A production-ready job marketplace REST API built with FastAPI, SQLAlchemy ORM, Pydantic validation, and PostgreSQL. Designed as a unified backend service for posting job listings, candidate applications, role searching, and platform analytics.

---

## 🛠️ Features & Concepts Implemented

- **Job Management:** CRUD endpoints for job listings (Title, Description, Location, Salary Range, Company Name, Role Type).
- **Advanced Search & Filtering:** Filter job listings dynamically by role, location, and salary threshold.
- **Candidate Applications:** Endpoints for candidates to submit applications to active job postings.
- **Analytics Dashboard:** Metrics endpoints calculating total jobs posted, candidate application counts, and role distributions.
- **Security & Data Quality:** JWT-based authentication for recruiters, strict Pydantic v2 data validation, and API rate limiting.
- **Interactive API Documentation:** Built-in Swagger UI and ReDoc for direct endpoint testing.

---

## 📋 Prerequisites

Before running the project locally, ensure you have the following installed:
- **Python 3.10+**
- **Git**
- **PostgreSQL Database** (Local instance or Neon.tech Cloud Connection)

---

## 🚀 How to Run Locally (Step-by-Step Guide)

### 1. Clone the Repository
Open your Terminal or Command Prompt and run:
```bash
git clone [https://github.com/hinacsag001-sudo/job-board-api.git](https://github.com/hinacsag001-sudo/job-board-api.git)
cd job-board-api
