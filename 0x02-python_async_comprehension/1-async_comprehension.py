#!/usr/bin/env python3
"""
Module 1-async_comprehension
"""
import asyncio
import random
from typing import List

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """
    Returns
    --------
    List
        10 random numbers
    """
    return [n async for n in async_generator()]
