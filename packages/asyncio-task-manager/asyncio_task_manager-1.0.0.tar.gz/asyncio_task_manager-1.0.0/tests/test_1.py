import asyncio

from asyncio_task_manager import TaskManager


async def task1():
    print("Running task 1")
    await asyncio.sleep(1)
    print("Task 1 completed")


async def task2():
    print("Running task 2")
    await asyncio.sleep(2)
    print("Task 2 completed")


async def task3():
    print("Running task 3")
    await asyncio.sleep(1)
    print("Task 3 completed")


async def test_TaskManager():
    task_manager = TaskManager(max_threads=2)

    task_manager.create_task("task1", task1)
    task_manager.create_task("task2", task2)
    task_manager.create_task("task3", task3)

    task_manager.add_dependency("task2", "task1")
    task_manager.add_dependency("task3", "task1")

    await task_manager.run_tasks()
