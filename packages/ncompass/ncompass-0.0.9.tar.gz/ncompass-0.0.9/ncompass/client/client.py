import os
import asyncio
from typing import Optional, Union, Generator

import ncompass.client.functional as F
from ncompass.network_utils import exec_url
from ncompass.errors import api_key_not_set, cannot_set_event_loop

class nCompass():
    def __init__(self
                 , api_key: Optional[str] = None
                 , custom_env_var: Optional[str] = None
                 , loop = None
                 , api_url = None):
        assert not ((api_key is not None) and (custom_env_var is not None))\
            ,'Cannot have both api_key and custom_env_var set'

        # NOTE: Be very careful what state this class holds as holding too much state might make it
        # hard to use nCompassOLOC well.
        
        self.api_key = None
        self.set_api_url(api_url)
        self.set_event_loop(loop)
        
        if api_key is not None:          self.api_key = api_key
        elif custom_env_var is not None: self.api_key = os.environ.get(custom_env_var)
        else:                            self.api_key = os.environ.get('NCOMPASS_API_KEY')
        
        if self.api_key is None: api_key_not_set(custom_env_var)

    def set_api_url(self, url=None):
        self.exec_url = url if url is not None else exec_url()

    def set_event_loop(self, event_loop=None):
        try:
            self.event_loop = event_loop if event_loop is not None else asyncio.get_event_loop()
        except RuntimeError as e:
            cannot_set_event_loop(str(e))

    def start_session(self):
        self.session = F.start_session(self.exec_url, self.api_key, self.event_loop) 
        self.wait_until_model_running()
    
    def stop_session(self):
        return F.stop_session(self.exec_url, self.api_key, self.session, self.event_loop) 

    def model_is_running(self):
        return F.model_is_running(self.exec_url, self.api_key)

    def wait_until_model_running(self) :
        F.wait_until_model_running(self.exec_url, self.api_key)

    def complete_prompt(self
                        , prompt
                        , max_tokens=300
                        , temperature=0.5
                        , top_p=0.9
                        , stream=True):
        res = F.complete_prompt( self.session
                                 , self.exec_url
                                 , self.api_key
                                 , prompt
                                 , max_tokens
                                 , temperature
                                 , top_p
                                 , stream 
                                 , self.event_loop)
        return res

    def complete_chat(self
                      , messages
                      , add_generation_prompt
                      , template_type=None
                      , max_tokens=300
                      , temperature=0.5
                      , top_p=0.9
                      , stream=True):
        return F.complete_chat(self.session
                               , self.exec_url
                               , self.api_key
                               , messages
                               , template_type
                               , add_generation_prompt
                               , max_tokens
                               , temperature
                               , top_p
                               , stream
                               , self.event_loop)

    def print_prompt(self, response_iterator):
        return F.print_prompt(response_iterator)

class nCompassOLOC():
    client = None
    event_loop = None
    #NOTE: Not thread safe!!

    @classmethod
    def set_event_loop(cls, event_loop):
        cls.event_loop = event_loop

    @classmethod
    def start_client(cls, api_key):
        if (cls.client is None) or (cls.client.api_key != api_key):
            cls.client = nCompass(api_key=api_key, loop=cls.event_loop)

    @classmethod
    def start_session(cls, api_key):
        cls.start_client(api_key)
        cls.client.start_session()
        cls.client.wait_until_model_running()
    
    @classmethod
    def stop_session(cls, api_key):
        cls.start_client(api_key)
        return cls.client.stop_session()
    
    @classmethod
    def complete_prompt(cls
                        , api_key
                        , prompt
                        , max_tokens=300
                        , temperature = 0.5
                        , top_p = 0.9
                        , stream = True
                        , pprint = False) -> Union[None, Generator]:
        cls.start_client(api_key)
        iterator = cls.client.complete_prompt(prompt
                                              , max_tokens
                                              , temperature
                                              , top_p
                                              , stream)
        if (stream and pprint): return F.print_prompt(iterator)
        else:                   return iterator # prompt in case of stream=false else iterator 

    @classmethod
    def complete_chat(cls
                      , api_key
                      , messages
                      , add_generation_prompt
                      , template_type = None
                      , max_tokens=300
                      , temperature = 0.5
                      , top_p = 0.9
                      , stream = True
                      , pprint = False) -> Union[None, Generator]:
        cls.start_client(api_key)
        iterator = cls.client.complete_chat(messages
                                            , add_generation_prompt
                                            , template_type
                                            , max_tokens
                                            , temperature
                                            , top_p
                                            , stream)
        if (stream and pprint): return F.print_prompt(iterator)
        else:                   return iterator # prompt in case of stream=false else iterator 
    
    @classmethod
    def print_response(cls, iterator):
        return F.print_prompt(iterator)
