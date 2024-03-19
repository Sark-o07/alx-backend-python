#!/usr/bin/env python3

"""
Module 2-measure_runtime
"""
import asyncio
import time

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Parameters
    ----------
    n : int
      number of times wait_random function called
    max_delay : int
      number of maximum delay

    Returns
    -------
    Float
        total execution time divied by n
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = time.perf_counter()

    return (end - start) / n
