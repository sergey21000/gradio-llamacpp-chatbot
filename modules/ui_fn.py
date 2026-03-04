import copy
import pprint
from typing import Iterator

import gradio as gr
from llama_cpp_py import LLMFormatter

from config import Config
from modules.llm import llm_client
from modules.logger import logger


CHAT_HISTORY = list[dict[str, str | list]]


class UiFn:
    def user_message_to_chatbot(
        user_message: dict[str, str | list[str]],
        chatbot: CHAT_HISTORY,
    ) -> tuple[str, CHAT_HISTORY]:
        if len(chatbot) > 0 and chatbot[-1]['role'] == 'user':
            chatbot = chatbot[:-1]
        user_msg = {'role': 'user', 'content': []}
        for file in user_message['files']:
            user_msg['content'].append(dict(path=file, type='file'))
        if user_message['text'] is not None:
            user_msg['content'].append(dict(text=user_message['text'], type='text'))
        chatbot.append(user_msg)
        logger.debug(f'"chatbot" in output "user_message_to_chatbot":\n{pprint.pformat(chatbot)}')
        return gr.update(value=None), chatbot

    @classmethod
    def llm_response_to_chatbot(
        cls,
        chatbot: CHAT_HISTORY,
        config: Config,
    ) -> Iterator[CHAT_HISTORY]:
        logger.debug(f'"chatbot" in input "yield_chatbot_with_llm_response":\n{pprint.pformat(chatbot)}')
        user_message = chatbot[-1]['content'][-1]['text']
        conf_kw = config.generation_kwargs
        if not user_message.strip():
            yield chatbot[:-1]
            return
        if not llm_client.check_health():
            msg = 'llm_client.check_health() failed'
            gr.Info(msg)
            logger.debug(msg)
            yield chatbot[:-1]
            return
        if Config.USE_RESPONSES_API:
            get_kwargs_method = config.get_responses_kwargs
        else:
            get_kwargs_method = config.get_completions_kwargs
        request_kwargs = get_kwargs_method(
            max_output_tokens=conf_kw['max_output_tokens'],
            enable_thinking=conf_kw['enable_thinking'],
            temperature=conf_kw['temperature'],
            top_p=conf_kw['top_p'],
            top_k=conf_kw['top_k'],
            repeat_penalty=conf_kw['repeat_penalty'],
        )
        if not conf_kw['do_sample']:
            request_kwargs['top_p'] = 0.0
            request_kwargs['extra_body']['top_k'] = 1
            request_kwargs['extra_body']['repeat_penalty'] = 1.0
        image_path = None
        file = chatbot[-1]['content'][0].get('file')
        if file:
            image_path = file.get('path')
            if not llm_client.check_multimodal_support():
                image_path = None
                warning_msg = (
                    'MMPROJ environment variable not set. '
                    'Image processing disabled. Skipping request.'
                )
                logger.warning(warning_msg)
                gr.Info(warning_msg)
                yield chatbot[:-1]
                return
        logger.debug(f'"chatbot" before "LLMFormatter.prepare_gradio_chatbot_messages":\n{pprint.pformat(chatbot)}')
        messages = LLMFormatter.prepare_gradio_chatbot_messages_to_openai(
            system_prompt=conf_kw['system_prompt'],
            support_system_role=Config.SUPPORT_SYSTEM_ROLE,
            history_len=conf_kw['history_len'],
            user_message=user_message,
            chatbot=chatbot,
            image_path=image_path,
            resize_size=Config.IMAGE_RESIZE_SIZE,
            convert_to_openai_format=True,
            use_responses_api=Config.USE_RESPONSES_API,
        )

        log_messags = copy.deepcopy(messages)
        for msg in log_messags:
            if isinstance(msg.get('content'), list):
                if msg['content'][0].get('input_image'):
                    msg['content'][0]['image_url'] = msg['content'][0]['image_url'][:30] + '...'
                elif msg['content'][0].get('image_url'):
                    msg['content'][0]['image_url']['url'] = msg['content'][0]['image_url']['url'][:30] + '...'

        logger.debug(f'"messages" before "llm_client.stream":\n{pprint.pformat(log_messags)}')
        logger.debug(f'"request_kwargs" before "llm_client.stream":\n{pprint.pformat(request_kwargs)}')
        stream_kwargs = dict(
            user_message_or_messages=messages,
            show_thinking=conf_kw['show_thinking'],
            return_per_token=True,
            out_token_in_thinking_mode='Thinking ...',
            use_responses_api=Config.USE_RESPONSES_API,
        )
        if Config.USE_RESPONSES_API:
            stream_kwargs['responses_kwargs'] = request_kwargs
        else:
            stream_kwargs['completions_kwargs'] = request_kwargs
        generator = llm_client.stream(**stream_kwargs)
        chatbot.append(dict(role='assistant', content=''))
        try:
            for token in generator:
                chatbot[-1]['content'] += token
                yield chatbot
        except Exception as ex:
            msg = f'Error generating LLM response: {ex}'
            gr.Info(msg)
            logger.exception(msg)
            yield chatbot[:-2]
            return


