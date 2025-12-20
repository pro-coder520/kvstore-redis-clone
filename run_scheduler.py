import time
import os
import sys
import django
from django.core.management import call_command


# Make sure this matches the name of the folder containing settings.py
# If your project is named 'redis_clone', this should be 'redis_clone.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kvstore.settings")
django.setup()

def run_scheduler():
    print("---------------------------------------------------")
    print("Scheduler Started. Running 'cleanup_keys' every 60s.")
    print("Press Ctrl+C to stop.")
    print("---------------------------------------------------")

    while True:
        try:
            # Run the management command we wrote earlier
            print(f"[{time.strftime('%X')}] Running cleanup...")
            call_command('cleanup_keys')
            
            # Wait for 60 seconds
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")
            sys.exit()
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_scheduler()