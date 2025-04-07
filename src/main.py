from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
from random import randint
from wheel import Result, Color, spin


config = {
    "maxTasks": 5,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


def handle_spin(task: ExternalTask) -> TaskResult:
    money = task.get_variable("money")
    bet_amount = task.get_variable("bet_amount")
    result = spin()

    mul = check_result(task, result)

    return task.complete({"money": bet_amount * mul + money})


def check_result(task: ExternalTask, result: Result) -> int:
    bet = task.get_variable("radio_options")
    match bet:
        case "NUMBER":
            bet_number = task.get_variable("bet_number")

            if (result.num == bet_number):
                return 35
            else:
                return -1
        case "BLACK":
            return 1 if result.color == Color.BLACK else -1 

        case "RED":
            return 1 if result.color == Color.RED else -1
        
        case "GREEN":
            return 35 if result.color == Color.GREEN else -1

        case "EVEN":
            return 1 if result.is_even else -1

        case "UNEVEN":
            return 1 if not result.is_even else -1
        
        case _:
            raise task.bpmn_error("please enter a valid option")


def main(): 
    worker = ExternalTaskWorker(worker_id="1", config=config)
    worker.subscribe("spin", handle_spin)


if __name__ == "__main__":
    main()

