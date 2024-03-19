#!/usr/bin/env python3

"""
Module 4-task
"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Parameters
    ----------
    n : int
      number of times wait_random function called
    max_delay : int
      number of maximum delay

    Returns
    -------
    List
        a list of delays in ascending order
    """
    tasks: List = []
    delays: List[float] = []
    for _ in range(n):
        tasks.append(task_wait_random(max_delay))

    for task in asyncio.as_completed(tasks):
        delays.append(await task)
    return delays
