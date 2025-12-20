Django HTTP Key-Value Store (Redis Clone)
A lightweight, high-performance Key-Value store built with Django. This project mimics the core functionality of Redis—allowing you to store, retrieve, and expire data—but uses HTTP requests instead of the RESP protocol, making it universally accessible via any REST client.

 Features
JSON-First: Store strings, integers, lists, or complex dictionaries natively using Django's JSONField.

Time-To-Live (TTL): Supports setting expiration times (in seconds) for any key.

Lazy Expiration: Automatically checks and removes expired keys when they are accessed.

Active Cleanup: Includes a custom background scheduler (run_scheduler.py) to physically purge stale data from the database every minute.

Atomic Operations: Uses database locking (update_or_create) to handle race conditions during concurrent writes.

 Installation & Setup
1. Prerequisites
Python 3.8+

Django 4.0+

2. Setup
Clone the repository and install the dependencies (Django):

Bash

pip install django
3. Database Initialization
Initialize the SQLite database (or Postgres if configured):

Bash

python manage.py makemigrations
python manage.py migrate
4. Run the Server
Start the main API server on port 8000:

Bash

python manage.py runserver 8000
 API Documentation
The store exposes a simple REST interface. You can use curl, Postman, or any HTTP client.

1. SET a Key
Create or update a key. You can optionally provide a ttl (Time-To-Live) in seconds.

Endpoint: POST /<key>/

Headers: Content-Type: application/json

Example: Store User Data (No Expiry)

Bash

curl -X POST http://127.0.0.1:8000/user:101/ \
     -H "Content-Type: application/json" \
     -d '{"value": {"name": "Emeka", "role": "Engineer", "skills": ["Python", "Django"]}}'
Example: Store an OTP (Expires in 60 seconds)

Bash

curl -X POST http://127.0.0.1:8000/otp:555/ \
     -H "Content-Type: application/json" \
     -d '{"value": 849201, "ttl": 60}'
2. GET a Key
Retrieve a value. If the key has expired, it will return a 404 and delete the record.

Endpoint: GET /<key>/

Example:

Bash

curl http://127.0.0.1:8000/user:101/
Response (Success):

JSON

{
    "key": "user:101",
    "value": {"name": "Emeka", "role": "Engineer", "skills": ["Python", "Django"]},
    "ttl_remaining": -1
}
Response (Expired/Missing):

JSON

{
    "error": "Key not found (expired)"
}
 Background Scheduler (Windows Compatible)
To prevent the database from filling up with expired keys that are never accessed (and thus never triggered for "Lazy Expiration"), this project includes a standalone scheduler.

How it works
The run_scheduler.py script runs in a loop, triggering the Django management command cleanup_keys every 60 seconds.

How to Run
Open a separate terminal window (keep your runserver running in the first one) and execute:

Bash

python run_scheduler.py
Output:

Plaintext

---------------------------------------------------
Scheduler Started. Running 'cleanup_keys' every 60s.
Press Ctrl+C to stop.
---------------------------------------------------
[14:05:01] Running cleanup...
Successfully deleted 12 expired keys
[14:06:01] Running cleanup...
 Project Structure
Bash

redis_clone/
├── db.sqlite3           # The database (persisted storage)
├── manage.py            # Django entry point
├── run_scheduler.py     # The background task runner
├── redis_clone/         # Project settings
│   ├── settings.py
│   └── urls.py
└── store/               # The Main App
    ├── models.py        # KeyValue model definition
    ├── views.py         # API logic (GET/POST)
    └── management/
        └── commands/
            └── cleanup_keys.py # Custom command for the scheduler