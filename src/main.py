from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
from random import randint


config = {
    "maxTasks": 5,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


def handle_spin(task: ExternalTask) -> TaskResult:
    num = randint(0, 36)
    return task.complete({"result": num})


def main(): 
    worker = ExternalTaskWorker(worker_id="1", config=config)
    worker.subscribe("spin", handle_spin)


if __name__ == "__main__":
    main()

