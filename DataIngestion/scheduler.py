import asyncio
from typing import Any, Coroutine

async def run_parallel(cors: list[Coroutine[Any, Any, None]], parallel_tasks: int = 10) -> None:
    running_tasks: list[asyncio.Task[None]] = []

    while len(cors) > 0:
        while len(cors) > 0 and len(running_tasks) < parallel_tasks:
            task = asyncio.create_task(cors.pop())
            running_tasks.append(task)
        await asyncio.sleep(1)
        running_tasks = _remove_completed_tasks(running_tasks)

    while len(running_tasks) > 0:
        running_tasks = _remove_completed_tasks(running_tasks)
        await asyncio.sleep(1)

def _remove_completed_tasks(running_tasks: list[asyncio.Task[None]]) -> list[asyncio.Task[None]]:
    remaining_tasks: list[asyncio.Task[None]] = []
    for task in running_tasks:
        if task.done():
            task.result() # re-raises any exception
        else:
            remaining_tasks.append(task)
    return remaining_tasks
