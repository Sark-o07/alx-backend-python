#!/usr/bin/env python3

"""
Module 1-concurrent_coroutines
"""
import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
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
        tasks.append(wait_random(max_delay))

    for task in asyncio.as_completed(tasks):
        delays.append(await task)
    return delays
