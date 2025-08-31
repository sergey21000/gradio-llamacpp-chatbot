import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from typing import Iterator

import pytest
import gradio as gr
from llama_cpp import Llama

import test_config


CHAT_HISTORY = list[gr.ChatMessage | dict[str, str | gr.Component]]


@pytest.fixture(autouse=True)
def patched_config(monkeypatch):
    monkeypatch.setattr(
        'config.LLAMA_MODEL_KWARGS',
        test_config.LLAMA_MODEL_KWARGS,
    )
    monkeypatch.setattr('config.SHOW_THINKING', test_config.SHOW_THINKING)


@pytest.fixture
def chatbot_with_message():
    from utils import user_message_to_chatbot

    chatbot = []
    user_message = 'Как дела?'
    result, updated_chatbot = user_message_to_chatbot(user_message, chatbot)
    assert len(updated_chatbot) == 1, 'The message was not added to the chat'
    assert result == ''
    assert updated_chatbot[-1]['role'] == 'user'
    assert updated_chatbot[-1]['content'] == user_message
    
    return updated_chatbot


def test_llm_pipepline(chatbot_with_message, monkeypatch):
    from utils import user_message_to_chatbot, bot_response_to_chatbot
    from config import GENERATION_KWARGS

    system_prompt = ''
    history_len = 0
    do_sample = True
    generate_args = list(GENERATION_KWARGS.values())
    stream_chatbot: Iterator[CHAT_HISTORY] = bot_response_to_chatbot(
        chatbot_with_message,
        system_prompt,
        history_len,
        do_sample,
        *generate_args,
    )
    for result_chatbot in stream_chatbot:
        pass
    assistant_message: str = result_chatbot[-1].get('content', '')
    assert len(assistant_message) > 0, 'LLM did not respond'
    print(f'Chatbot response: {assistant_message}')