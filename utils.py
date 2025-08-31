from pathlib import Path
from typing import Union, List, Dict, Tuple, Optional
from tqdm import tqdm

import requests
from llama_cpp import Llama
import gradio as gr

from config import GENERATE_KWARGS
from init_model import MODEL, SUPPORT_SYSTEM_ROLE 


CHAT_HISTORY = List[Optional[Dict[str, Optional[str]]]]


def user_message_to_chatbot(user_message: str, chatbot: CHAT_HISTORY) -> Tuple[str, CHAT_HISTORY]:
    if user_message:
        chatbot.append({'role': 'user', 'content': user_message})
    return '', chatbot


def bot_response_to_chatbot(
        chatbot: CHAT_HISTORY,
        system_prompt: str,
        history_len: int,
        do_sample: bool,
        *generate_args,
        ):

    if len(chatbot) == 0 or chatbot[-1]['role'] == 'assistant':
        yield chatbot
        return

    messages = []
    if SUPPORT_SYSTEM_ROLE and system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})

    if history_len != 0:
        messages.extend(chatbot[:-1][-(history_len*2):])

    messages.append(chatbot[-1])

    gen_kwargs = dict(zip(GENERATE_KWARGS.keys(), generate_args))
    gen_kwargs['top_k'] = int(gen_kwargs['top_k'])
    if not do_sample:
        gen_kwargs['top_p'] = 0.0
        gen_kwargs['top_k'] = 1
        gen_kwargs['repeat_penalty'] = 1.0

    stream_response = MODEL.create_chat_completion(
        messages=messages,
        stream=True,
        **gen_kwargs,
        )

    chatbot.append({'role': 'assistant', 'content': ''})
    is_think = False
    for chunk in stream_response:
        token = chunk['choices'][0]['delta'].get('content')
        if token is not None:
            if token == '<think>':
                is_think = True
                gr.Info('Thinking...')
            elif token == '</think>':
                is_think = False
            if not is_think:
                chatbot[-1]['content'] += token
            yield chatbot

