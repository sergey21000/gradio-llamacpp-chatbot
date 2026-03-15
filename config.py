import os
import sys
from typing import Any


class Config:
    IMAGE_RESIZE_SIZE: int | None = 512
    SUPPORT_SYSTEM_ROLE: bool = True
    LLAMACPP_RELEASE_TAG: str = os.getenv('LLAMACPP_RELEASE_TAG', 'latest')
    LLAMACPP_PREFER_CUDA_BUILD: bool = (
        os.getenv('LLAMACPP_PREFER_CUDA_BUILD', 'true').lower()
        in ('true', '1')
    )
    USE_RESPONSES_API = (
        os.getenv('CHATBOT_USE_RESPONSES_API', '0').lower() 
        in ('1', 'true')
    )

    def __init__(self):
        self.generation_kwargs = dict(
            max_output_tokens=-1,
            do_sample=True,
            temperature=0.2,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.0,
            system_prompt='',
            history_len=0,
            enable_thinking=False,
            show_thinking=False,
        )

    @staticmethod
    def get_responses_kwargs(**kwargs) -> dict[str, Any]:
        return dict(
            temperature=kwargs['temperature'],
            top_p=kwargs['top_p'],
            max_output_tokens=kwargs['max_output_tokens'],
            extra_body=dict(
                top_k=kwargs['top_k'],
                repeat_penalty=kwargs['repeat_penalty'],
                reasoning_format='none',
                chat_template_kwargs=dict(
                    enable_thinking=kwargs['enable_thinking'],
                ),
            ),
        )
    
    @classmethod
    def get_completions_kwargs(cls, **kwargs) -> dict[str, Any]:
        completions_kwargs = cls.get_responses_kwargs(**kwargs)
        max_output_tokens = completions_kwargs.pop('max_output_tokens', -1)
        completions_kwargs['max_tokens'] = max_output_tokens
        return completions_kwargs


class UiGradioConfig:
    '''Gradio settings for gr.Blocks()'''
    css: str | None = '''
    .gradio-container {
        width: 70% !important;
        margin: 0 auto !important;
    }
    '''
    if hasattr(sys, 'getandroidapilevel') or 'ANDROID_ROOT' in os.environ:
        css = None
    theme: str | None = None
    fill_height: bool = False
    footer_links: list[str] = ['gradio', 'settings']
    delete_cache: tuple[int, int] | None = None

    @classmethod
    def get_demo_launch_kwargs(cls):
        return dict(
            css=cls.css,
            theme=cls.theme,
            footer_links=cls.footer_links,
        )

    @classmethod
    def get_demo_blocks_kwargs(cls):
        return dict(
            fill_height=cls.fill_height,
            delete_cache=cls.delete_cache,
        )
