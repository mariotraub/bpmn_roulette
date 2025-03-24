import requests
import json
import time
import random

CAMUNDA_BASE_URL = "http://localhost:8080/engine-rest"
WORKER_ID = "python_worker_1"

def fetch_task():
    url = f"{CAMUNDA_BASE_URL}/external-task/fetchAndLock"
    payload = {
        "workerId": WORKER_ID,
        "maxTasks": 1,
        "topics": [{"topicName": "spin", "lockDuration": 10000}]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        tasks = response.json()
        return tasks[0] if tasks else None
    print("Error fetching task:", response.text)
    return None

def spin_roulette():
    return str(random.randint(0, 36))

def complete_task(task_id, result):
    url = f"{CAMUNDA_BASE_URL}/external-task/{task_id}/complete"
    payload = {
        "workerId": WORKER_ID,
        "variables": {
            "spinResult": {"value": result, "type": "String"}
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code == 204:
        print("Task completed successfully")
    else:
        print("Error completing task:", response.text)

def worker_loop():
    while True:
        print("Polling for tasks...")
        task = fetch_task()
        if not task:
            print("No tasks available, waiting...")
            time.sleep(5)
            continue
        
        print(f"Processing task {task['id']}")
        outcome = spin_roulette()
        print(f"Task outcome: {outcome}")
        complete_task(task['id'], outcome)
        
if __name__ == "__main__":
    print("Starting Camunda external task worker...")
    worker_loop()
