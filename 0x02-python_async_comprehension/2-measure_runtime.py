#!/usr/bin/env python3
"""
Module 2-measure_runtime
"""
import asyncio
import time


async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    Returns
    --------
    flaot
        total runtime
    """
    start = time.perf_counter()
    await asyncio.gather(async_comprehension(),
                         async_comprehension(),
                         async_comprehension(),
                         async_comprehension())
    return time.perf_counter() - start
