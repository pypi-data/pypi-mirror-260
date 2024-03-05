import json

from ncompass.errors import error_msg
from ncompass.network_utils import async_streaming_post_json
from ncompass.async_utils import run_in_event_loop, get_sync_generator_from_async

def build_prompt_body_from_params(prompt
                                  , miid
                                  , max_tokens
                                  , temperature
                                  , top_p
                                  , stream):
    body = {'prompt':        prompt
            , 'miid':        miid
            , 'max_tokens':  max_tokens
            , 'temperature': temperature
            , 'top_p':       top_p
            , 'stream':      stream}
    return body

async def response_generator(response):
    response_len = 0
    async for chunk, _ in response.content.iter_chunks():
        try:
            split_chunk = chunk.split(b'\0')
            decoded_chunk = split_chunk[0].decode('utf-8')
            try:
                data = json.loads(decoded_chunk)
                res = data['text'][0] 
                new_data = res[response_len:]
                response_len = len(res)
                yield new_data
            except Exception as e:
                yield ''
        except Exception as e:
            error_msg(str(e))

async def stream_response_handler(response):
    if response.status == 200:
       return response_generator(response)
    else:
        res = await response.json()
        error_msg(res['error'])

async def batch_response_handler(response):
    res = await response.json(content_type=None)
    if response.status == 200:
        return res['text']
    elif response.status == 499:
        error_msg("Client connection was lost on server: {res['error']}")
    elif response.status == 400:
        error_msg(f"Server failed to generate response: {res['error']}")
    else:
        error_msg(res['error'])

def run_completion(session
                   , url: str
                   , miid: str
                   , prompt: str
                   , max_tokens: int
                   , temperature: float
                   , top_p: float
                   , stream: bool
                   , event_loop=None):
    _url = f'{url}/run_prompt'
    headers = {'Content-Type': "application/json", 'Authorization': miid} 
    body = build_prompt_body_from_params(prompt, miid, max_tokens, temperature, top_p, stream) 
    if stream:
        res = run_in_event_loop(async_streaming_post_json(session
                                                          , _url
                                                          , body
                                                          , headers
                                                          , stream_response_handler), event_loop)
        return get_sync_generator_from_async(res, event_loop)
    else:
        return run_in_event_loop(async_streaming_post_json(session
                                                           , _url
                                                           , body
                                                           , headers
                                                           , batch_response_handler), event_loop)

def build_chat_body_from_params(messages
                                , template_type
                                , add_generation_prompt
                                , miid
                                , max_tokens
                                , temperature
                                , top_p
                                , stream):
    body = {'messages':                messages
            , 'template':              template_type
            , 'add_generation_prompt': add_generation_prompt
            , 'miid':                  miid
            , 'max_tokens':            max_tokens
            , 'temperature':           temperature
            , 'top_p':                 top_p
            , 'stream':                stream}
    return body

def run_chat_completion(session
                        , url: str
                        , miid: str
                        , messages: str
                        , template_type
                        , add_generation_prompt
                        , max_tokens: int
                        , temperature: float
                        , top_p: float
                        , stream: bool
                        , event_loop=None):
    _url = f'{url}/run_prompt'
    headers = {'Content-Type': "application/json", 'Authorization': miid} 
    body = build_chat_body_from_params(messages
                                       , template_type
                                       , add_generation_prompt
                                       , miid
                                       , max_tokens
                                       , temperature
                                       , top_p
                                       , stream) 
    if stream:
        res = run_in_event_loop(async_streaming_post_json(session
                                                          , _url
                                                          , body
                                                          , headers
                                                          , stream_response_handler), event_loop)
        return get_sync_generator_from_async(res, event_loop)
    else:
        return run_in_event_loop(async_streaming_post_json(session
                                                           , _url
                                                           , body
                                                           , headers
                                                           , batch_response_handler), event_loop)
