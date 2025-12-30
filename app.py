import os
import sys

import gradio as gr

from config import GENERATION_KWARGS, SHOW_THINKING
from utils import (
    user_message_to_chatbot,
    bot_response_to_chatbot,
)
from init_model import SUPPORT_SYSTEM_ROLE

from dotenv import load_dotenv
load_dotenv(dotenv_path='gradio_env')


def get_system_prompt_component(interactive: bool) -> gr.Textbox:
    value = '' if interactive else 'System prompt is not supported by this model'
    return gr.Textbox(value=value, label='System prompt', interactive=interactive)


def get_generation_args(do_sample: bool) -> list[gr.Component]:
    KW = GENERATION_KWARGS
    generation_args = [
        gr.Slider(minimum=0.1, maximum=3, value=KW['temperature'], step=0.1, label='temperature', visible=do_sample),
        gr.Slider(minimum=0, maximum=1, value=KW['top_p'], step=0.01, label='top_p', visible=do_sample),
        gr.Slider(minimum=1, maximum=50, value=KW['top_k'], step=1, label='top_k', visible=do_sample),
        gr.Slider(minimum=1, maximum=5, value=KW['repeat_penalty'], step=0.1, label='repeat_penalty', visible=do_sample),
    ]
    return generation_args


css = '''
.gradio-container {
    width: 70% !important;
    margin: 0 auto !important;
}
'''

if hasattr(sys, 'getandroidapilevel') or 'ANDROID_ROOT' in os.environ:
    css = None

with gr.Blocks(css=css) as interface:
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown('Новая фича')
            chatbot = gr.Chatbot(
                type='messages',
                show_copy_button=True,
                sanitize_html=False if SHOW_THINKING else True,
                height=480,
            )
            user_message = gr.Textbox(label='User')
            with gr.Row():
                user_message_btn = gr.Button('Send')
                stop_btn = gr.Button('Stop')
                clear_btn = gr.Button('Clear')
            system_prompt = get_system_prompt_component(interactive=SUPPORT_SYSTEM_ROLE)

        with gr.Column(scale=1, min_width=80):
            with gr.Group():
                gr.Markdown('Length of message history')
                history_len = gr.Slider(
                    minimum=0,
                    maximum=10,
                    value=0,
                    step=1,
                    info='Number of previous messages taken into account in history',
                    label='history_len',
                    show_label=False,
               )
                with gr.Group():
                    gr.Markdown('Generation parameters')
                    do_sample = gr.Checkbox(
                        value=False,
                        label='do_sample',
                        info='Activate random sampling',
                    )
                    generation_args = get_generation_args(do_sample.value)
                    do_sample.change(
                        fn=get_generation_args,
                        inputs=do_sample,
                        outputs=generation_args,
                        show_progress=False,
                    )

    generate_event = gr.on(
        triggers=[user_message.submit, user_message_btn.click],
        fn=user_message_to_chatbot,
        inputs=[user_message, chatbot],
        outputs=[user_message, chatbot],
    ).then(
        fn=bot_response_to_chatbot,
        inputs=[chatbot, system_prompt, history_len, do_sample, *generation_args],
        outputs=[chatbot],
    )
    stop_btn.click(
        fn=None,
        inputs=None,
        outputs=None,
        cancels=[generate_event],
    )
    clear_btn.click(
        fn=lambda: None,
        inputs=None,
        outputs=[chatbot],
    )


if __name__ == '__main__':

    interface.launch()

