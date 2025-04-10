from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
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
    money: int = int(task.get_variable("money"))
    bet_amount: int = int(task.get_variable("bet_amount"))
    result = spin()

    try:
        mul = check_result(task, result)
        won = bool(mul > 0)
    except ValueError as e:
        return task.bpmn_error("INVALID_BET", str(e))

    new_money = money + bet_amount * mul
    return task.complete({
        "money": new_money,
        "won": won,
    })


def check_result(task: ExternalTask, result: Result) -> int:
    bet: str = str(task.get_variable("radio_options"))
    match bet:
        case "NUMBER":
            bet_number = task.get_variable("bet_number")
            
            return 35 if result.num == bet_number else -1
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
            raise ValueError("Enter a valid option")

def main(): 
    worker = ExternalTaskWorker(worker_id="1", config=config)
    worker.subscribe("spin", handle_spin)


if __name__ == "__main__":
    main()

