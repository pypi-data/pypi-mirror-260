import json
import aiohttp
import asyncio
from ncompass.errors import error_msg

def run_in_event_loop(coro, event_loop=None):
    if event_loop is None: event_loop = asyncio.get_event_loop()
    res = event_loop.run_until_complete(coro)
    return res

async def async_get_next(ait):
    try:
        obj = await ait.__anext__()
        return False, obj
    except StopAsyncIteration:
        return True, None

def get_sync_generator_from_async(async_gen, event_loop=None):
    ait = async_gen.__aiter__()
    # Event loop explictly set here for speed optimization. If even_loop isn't passed in, we don't
    # want to keep getting running loop every iteration of the while loop
    if event_loop is None: event_loop = asyncio.get_event_loop() 
    while True:
        done, res = run_in_event_loop(async_get_next(ait), event_loop)
        if done: break
        yield res
