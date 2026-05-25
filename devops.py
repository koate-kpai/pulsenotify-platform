#!/usr/bin/env python3
"""Master automation script for PulseNotify local CI cycle."""

import os
import subprocess
import time
import requests
import sys

# Check if we are in CI, use special Docker host URL if true
if os.environ.get("CI") == "true":
    API_URL = "http://host.docker.internal:8000"
else:
    API_URL = "http://localhost:8000"

# ... the rest of your devops.py remains exactly the same ...

API_HEALTH_URL = "http://localhost:8000/health"
MAX_RETRIES = 30
RETRY_DELAY = 2


def run_command(cmd, check=True):
    print(f"\n🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"❌ Command failed:\n{result.stderr}")
        sys.exit(result.returncode)
    return result


def start_stack():
    run_command(["docker", "compose", "up", "-d", "--build"])


def wait_for_healthy():
    print(f"\n⏳ Waiting for {API_HEALTH_URL} ...")
    for i in range(MAX_RETRIES):
        try:
            r = requests.get(API_HEALTH_URL, timeout=2)
            if r.status_code == 200:
                print("✅ API is healthy")
                return True
        except requests.ConnectionError:
            pass
        print(f"   Attempt {i+1}/{MAX_RETRIES} - not ready yet")
        time.sleep(RETRY_DELAY)
    print("❌ API did not become healthy")
    sys.exit(1)


def run_tests():
    run_command(["docker", "compose", "run", "--rm", "api", "pytest"])


def teardown():
    run_command(["docker", "compose", "down", "-v"], check=False)


if __name__ == "__main__":
    try:
        start_stack()
        wait_for_healthy()
        run_tests()
        print("\n🎉 All tests passed! Pipeline cycle complete.")
    finally:
        teardown()
        print("🧹 Stack torn down.")
