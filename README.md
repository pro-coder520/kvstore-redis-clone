# ⚡ Django-Redis: HTTP Key-Value Store

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-MVP-orange?style=for-the-badge)

A lightweight, high-performance **Key-Value Store** built entirely on the **Django** framework.

This project re-imagines Redis as a **RESTful web service**. It provides atomic `SET` and `GET` operations, supports complex `JSON` data types natively, and implements a robust **expiration engine** (TTL) that works both lazily (on-access) and actively (via a background scheduler).

---

## 📑 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Background Scheduler](#-background-scheduler)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🧐 About the Project

I built this project to demonstrate that Django can be used for more than just standard CRUD apps. By leveraging Django's **ORM** for atomic locking (`update_or_create`) and `JSONField` for flexible storage, we created a **thread-safe state store** that can be accessed by any HTTP client.

It is designed to be a **"State Microservice"** for distributed systems that need to share configuration or session data without setting up a full Redis instance.

---

## ✨ Key Features

* ✅ **JSON-First Storage:** Store `strings`, `lists`, `integers`, or nested `dictionaries` natively.
* ✅ **Time-To-Live (TTL):** Set keys to auto-expire after `N` seconds.
* ✅ **Lazy Expiration:** Expired keys are instantly detected and removed during `GET` requests.
* ✅ **Active Cleanup:** A standalone background worker purges stale data to keep the DB lean.
* ✅ **Atomic Writes:** Handles race conditions safely using database-level locking strategies.

---

## 🏗 Architecture

The system uses a **Hybrid Expiration Strategy**:

1. **Lazy Deletion (Passive):**  
   When a client requests a key via `GET`, the server checks `if now > expires_at`. If true, it deletes the key immediately and returns `404 Not Found`.

2. **Active Deletion (Active):**  
   A background script (`run_scheduler.py`) runs every **60 seconds** to bulk-delete keys that haven't been accessed recently but are past their expiry.

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.8+**
* `pip` (Python Package Manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-redis-clone.git
   cd django-redis-clone
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Initialize the Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the Server**
   ```bash
   python manage.py runserver 8000
   ```

---

## 🔌 Usage Guide

The API accepts and returns `application/json`. You can use `curl`, **Postman**, or any HTTP client.

### 1. SET a Value

Create or update a key.

#### Example A: Standard Storage (No Expiry)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/user-config/ \
     -H "Content-Type: application/json" \
     -d '{
           "value": {"theme": "dark", "notifications": true}
         }'
```

**Response:**
```json
{
    "status": "ok",
    "action": "created",
    "key": "user-config",
    "expires_at": null
}
```

#### Example B: Storage with TTL (Expires in 60s)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/otp-code/ \
     -H "Content-Type: application/json" \
     -d '{
           "value": 49201, 
           "ttl": 60
         }'
```

**Response:**
```json
{
    "status": "ok",
    "action": "created",
    "key": "otp-code",
    "expires_at": "2025-12-20T21:31:00Z"
}
```

### 2. GET a Value

Retrieve a key.

**Request:**
```bash
curl http://127.0.0.1:8000/user-config/
```

**Response (Success):**
```json
{
    "key": "user-config",
    "value": {"theme": "dark", "notifications": true},
    "ttl_remaining": -1
}
```

**Response (Expired or Missing):**
```json
{
    "error": "Key not found (expired)"
}
```

---

## 🕰 Background Scheduler

To prevent the database from growing infinitely with stale data, run the included scheduler. This script works on Windows, Linux, and macOS.

**Run in a separate terminal window:**
```bash
python run_scheduler.py
```

**Output:**
```
---------------------------------------------------
Scheduler Started. Running 'cleanup_keys' every 60s.
---------------------------------------------------
Running cleanup... Successfully deleted 5 expired keys.
```

---

## 📂 Project Structure

```
redis_clone/
├── db.sqlite3           # The persisted database
├── manage.py            # Django entry point
├── run_scheduler.py     # Background task runner (Custom Script)
├── redis_clone/         # Project Settings
│   ├── settings.py
│   └── urls.py
└── store/               # Main Application
    ├── models.py        # KeyValue model definition
    ├── views.py         # API logic (GET/POST)
    └── management/
        └── commands/
            └── cleanup_keys.py # The cleanup logic
```

---

## 🗺 Roadmap

- [x] Basic SET/GET operations
- [x] Lazy Expiration logic
- [x] Background Cleanup Scheduler
- [ ] Add Authentication (API Key middleware)
- [ ] Add INCR and DECR atomic operations for counters
- [ ] Dockerize the application with docker-compose

---

## 📄 License

Distributed under the MIT License. See LICENSE for more information.

---

## 👤 Author

Built with ❤️ by Iremide Joseph Adeyanju.
