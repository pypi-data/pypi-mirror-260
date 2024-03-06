import asyncio
from typing import Callable, Coroutine, Dict, List, Set


class TaskManager:
    def __init__(self, max_threads: int):
        self.max_threads = max_threads
        self.tasks: Dict[str, Coroutine] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.running_tasks: Set[str] = set()
        self.completed_tasks: Set[str] = set()

    def create_task(
        self, task_id: str, coroutine: Callable[..., Coroutine], *args, **kwargs
    ) -> None:
        """
        Create a new task with the given task ID and coroutine function.
        """
        self.tasks[task_id] = coroutine(*args, **kwargs)
        self.dependencies[task_id] = set()

    def add_dependency(self, task_id: str, dependency_id: str) -> None:
        """
        Add a dependency between two tasks.
        """
        self.dependencies[task_id].add(dependency_id)

    async def run_tasks(self) -> None:
        """
        Run all tasks in the dependency graph, respecting the maximum thread count.
        """
        while self.tasks:
            # Find tasks that have no pending dependencies
            ready_tasks = [
                task_id
                for task_id in self.tasks
                if self.dependencies[task_id].issubset(self.completed_tasks)
            ]

            # Run tasks concurrently, respecting the maximum thread count
            running_tasks = [
                asyncio.create_task(self._run_task(task_id))
                for task_id in ready_tasks[: self.max_threads]
            ]
            await asyncio.gather(*running_tasks)

    async def _run_task(self, task_id: str) -> None:
        """
        Run a single task and update the task states.
        """
        self.running_tasks.add(task_id)
        await self.tasks[task_id]
        self.running_tasks.remove(task_id)
        self.completed_tasks.add(task_id)
        del self.tasks[task_id]
        del self.dependencies[task_id]
