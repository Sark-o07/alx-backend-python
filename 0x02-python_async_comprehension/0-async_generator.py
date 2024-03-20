#!/usr/bin/env python3
"""
Module 0-async_generator
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    Returns
    --------
    asyncronous generator
        yeild a random number between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
