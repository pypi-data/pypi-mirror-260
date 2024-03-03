import time
import aiohttp
import asyncio
from datetime import datetime, timedelta

from .run_prompt import stream_prompt, stream_prompt_legacy
from ncompass.network_utils import get
from .model_health import check_model_health
from ncompass.errors import model_not_started

def run_in_loop(coro):
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)
    except:
        loop = asyncio.new_event_loop()
        return asyncio.run_coroutine_threadsafe(coro, loop).result()

def start_stop_handler(response):
    if (response.status_code == 200) or (response.status_code == 209): 
        return True
    elif (response.status_code == 400): 
        raise RuntimeError('Internal server error, contact admin@ncompass.tech')
    else: 
        raise RuntimeError(response.text)

async def close_session(session):
    return await session.close()

async def create_session():
    return aiohttp.ClientSession()

def start_session(url, api_key):
    session = run_in_loop(create_session())
    try:
        start_stop_handler(get(f'{url}/start_session', {'Authorization': api_key}))
        return session
    except Exception as e:
        run_in_loop(close_session(session))
        raise e

def stop_session(url, api_key, session):
    if session is not None: run_in_loop(close_session(session))
    return start_stop_handler(get(f'{url}/stop_session', {'Authorization': api_key}))

def model_is_running(url, api_key):
    try: # this try-catch looks for network connectivity issues with running check_model_health
        response = check_model_health(url, api_key)
    except Exception :
        return False
    if (response.status_code == 404):
        # Model is not in live models dictionary
        return False
    elif (response.status_code == 400):
        # Model is in live models dictionary, but not started (this is fine, just need to start
        # session)
        return True
    elif response.status_code == 200:
        return True
    elif response.status_code == 504:
        model_not_started(api_key)
    else:
        return False

def wait_until_model_running(url, api_key, timeout=20):
    break_loop = False
    wait_until = datetime.now() + timedelta(seconds=timeout)
    while not break_loop:
        if model_is_running(url, api_key): break_loop = True
        if wait_until < datetime.now(): 
            model_not_started(api_key)

def complete_prompt(session
                    , url
                    , api_key
                    , prompt
                    , max_tokens
                    , temperature
                    , top_p
                    , stream
                    , legacy=False):
    if not legacy:
        get_stream = lambda : stream_prompt(session
                                            , url=url
                                            , miid=api_key
                                            , prompt=prompt
                                            , max_tokens=max_tokens
                                            , temperature=temperature
                                            , top_p=top_p
                                            , stream=stream)
    else:
        get_stream = lambda : stream_prompt_legacy(url=url
                                                   , miid=api_key
                                                   , prompt=prompt
                                                   , max_tokens=max_tokens
                                                   , temperature=temperature
                                                   , top_p=top_p
                                                   , stream=stream)
    stream_iterator = get_stream()
    if stream: return stream_iterator
    else:      return ''.join(res for res in stream_iterator)
    
def print_prompt(response_iterator):
    [print(elem, end='', flush=True) for elem in response_iterator]
    print()
