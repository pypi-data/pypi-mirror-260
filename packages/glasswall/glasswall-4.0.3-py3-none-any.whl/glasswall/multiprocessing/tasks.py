from multiprocessing import Queue
from typing import Any, Callable, Optional, Union
from glasswall.multiprocessing.deletion import force_object_under_target_size


class Task:
    def __init__(
        self,
        func: Callable,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
    ):
        self.func = func
        self.args = args or tuple()
        self.kwargs = kwargs or dict()

    def __eq__(self, other):
        if isinstance(other, Task):
            return (self.func, self.args, self.kwargs) == (other.func, other.args, other.kwargs)
        return False

    def __hash__(self):
        kwargs_tuple = tuple(sorted(self.kwargs.items()))
        return hash((self.func, self.args, kwargs_tuple))

    def __repr__(self):
        args_str = ", ".join(map(repr, self.args))
        kwargs_str = ", ".join(f"{key}={value!r}" for key, value in self.kwargs.items())
        return (
            f"Task(func={self.func.__name__}, args=({args_str}), kwargs=({kwargs_str}))"
        )


class TaskResult:
    timeout_seconds: Optional[float]
    memory_limit_in_gb: Optional[float]
    start_time: float
    end_time: float
    elapsed_time: float
    out_of_memory: bool
    timed_out: bool

    def __init__(
        self,
        task: Task,
        success: bool,
        result: Any = None,
        exception: Union[Exception, None] = None,
    ):
        self.task = task
        self.success = success
        self.result = result
        self.exception = exception

    def __eq__(self, other):
        if isinstance(other, TaskResult):
            return (self.task, self.success, self.result, self.exception) == \
                (other.task, other.success, other.result, other.exception)
        return False

    def __hash__(self):
        return hash((self.task, self.success, self.result, self.exception))


def execute_task_and_put_in_queue(task: Task, queue: "Queue[TaskResult]") -> None:
    try:
        func_result = task.func(*task.args, **task.kwargs)
        task_result = TaskResult(task=task, success=True, result=func_result)
    except Exception as e:
        task_result = TaskResult(task=task, success=False, exception=e)

    # Ensure task_result can fit in queue
    task_result = force_object_under_target_size(task_result, target_size=8192)

    queue.put(task_result)
