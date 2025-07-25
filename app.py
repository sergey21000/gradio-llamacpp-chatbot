from pathlib import Path
from shutil import rmtree
from typing import Union, List, Dict, Tuple, Optional
from tqdm import tqdm

import requests
from llama_cpp import Llama
import gradio as gr



# ================== VARIABLES =============================

MODELS_PATH = Path('models')
MODELS_PATH.mkdir(exist_ok=True)
DEFAULT_GGUF_URL = 'https://huggingface.co/bartowski/google_gemma-3-1b-it-GGUF/resolve/main/google_gemma-3-1b-it-Q8_0.gguf'


GENERATE_KWARGS = dict(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    repeat_penalty=1.0,
    )

LLAMA_MODEL_KWARGS = dict(
    n_gpu_layers=-1,
    verbose=False,
    n_ctx=4096,
)

# ================== ANNOTATIONS ========================

CHAT_HISTORY = List[Optional[Dict[str, Optional[str]]]]
MODEL_DICT = Dict[str, Llama]


# ================== FUNCS =============================

def download_file(file_url: str, file_path: Union[str, Path]) -> None:
    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        raise Exception(f'Файл недоступен для скачивания по ссылке: {file_url}')
    total_size = int(response.headers.get('content-length', 0))
    progress_tqdm = tqdm(desc='Loading GGUF file', total=total_size, unit='iB', unit_scale=True)
    progress_gradio = gr.Progress()
    completed_size = 0
    with open(file_path, 'wb') as file:
        for data in response.iter_content(chunk_size=4096):
            size = file.write(data)
            progress_tqdm.update(size)
            completed_size += size
            desc = f'Loading GGUF file, {completed_size/1024**3:.3f}/{total_size/1024**3:.3f} GB'
            progress_gradio(completed_size/total_size, desc=desc)


def download_gguf_and_init_model(gguf_url: str, model_dict: MODEL_DICT) -> Tuple[MODEL_DICT, bool, str]:
    log = ''
    if not gguf_url.endswith('.gguf'):
        log += f'The link must be a direct link to the GGUF file\n'
        return model_dict, log

    gguf_filename = gguf_url.rsplit('/')[-1]
    model_path = MODELS_PATH / gguf_filename
    progress = gr.Progress()

    if not model_path.is_file():
        progress(0.3, desc='Шаг 1/2: Loading GGUF model file')
        try:
            download_file(gguf_url, model_path)
            log += f'Model file {gguf_filename} successfully loaded\n'
        except Exception as ex:
            log += f'Error loading model from link {gguf_url}, error code:\n{ex}\n'
            curr_model = model_dict.get('model')
            if curr_model is None:
                log += f'Model is missing from dictionary "model_dict"\n'
                return model_dict, load_log
            curr_model_filename = Path(curr_model.model_path).name
            log += f'Current initialized model: {curr_model_filename}\n'
            return model_dict, log
    else:
        log += f'Model file {gguf_filename} loaded, initializing model...\n'

    progress(0.7, desc='Шаг 2/2: Model initialization')
    model = Llama(model_path=str(model_path), **LLAMA_MODEL_KWARGS)
    model_dict = {'model': model}
    support_system_role = 'System role not supported' not in model.metadata['tokenizer.chat_template']
    log += f'Model {gguf_filename} initialized\n'
    return model_dict, support_system_role, log


def user_message_to_chatbot(user_message: str, chatbot: CHAT_HISTORY) -> Tuple[str, CHAT_HISTORY]:
    if user_message:
        chatbot.append({'role': 'user', 'content': user_message})
    return '', chatbot


def bot_response_to_chatbot(
        chatbot: CHAT_HISTORY,
        model_dict: MODEL_DICT,
        system_prompt: str,
        support_system_role: bool,
        history_len: int,
        do_sample: bool,
        *generate_args,
        ):

    model = model_dict.get('model')
    if model is None:
        gr.Info('Model not initialized')
        yield chatbot
        return

    if len(chatbot) == 0 or chatbot[-1]['role'] == 'assistant':
        yield chatbot
        return

    messages = []
    if support_system_role and system_prompt:
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

    stream_response = model.create_chat_completion(
        messages=messages,
        stream=True,
        **gen_kwargs,
        )

    chatbot.append({'role': 'assistant', 'content': ''})
    for chunk in stream_response:
        token = chunk['choices'][0]['delta'].get('content')
        if token is not None:
            chatbot[-1]['content'] += token
            yield chatbot


def get_system_prompt_component(interactive: bool) -> gr.Textbox:
    value = '' if interactive else 'System prompt is not supported by this model'
    return gr.Textbox(value=value, label='System prompt', interactive=interactive)


def get_generate_args(do_sample: bool) -> List[gr.component]:
    generate_args = [
        gr.Slider(minimum=0.1, maximum=3, value=GENERATE_KWARGS['temperature'], step=0.1, label='temperature', visible=do_sample),
        gr.Slider(minimum=0, maximum=1, value=GENERATE_KWARGS['top_p'], step=0.01, label='top_p', visible=do_sample),
        gr.Slider(minimum=1, maximum=50, value=GENERATE_KWARGS['top_k'], step=1, label='top_k', visible=do_sample),
        gr.Slider(minimum=1, maximum=5, value=GENERATE_KWARGS['repeat_penalty'], step=0.1, label='repeat_penalty', visible=do_sample),
    ]
    return generate_args


# =============== INIT MODEL =============================

start_model_dict, start_support_system_role, start_load_log = download_gguf_and_init_model(
    gguf_url=DEFAULT_GGUF_URL, model_dict={},
    )


# ================== INTERFACE =============================

theme = gr.themes.Base(primary_hue='green', secondary_hue='yellow', neutral_hue='zinc').set(
    loader_color='rgb(0, 255, 0)',
    slider_color='rgb(0, 200, 0)',
    body_text_color_dark='rgb(0, 200, 0)',
    button_secondary_background_fill_dark='green',
)

# css = None
css = '''
.gradio-container {
    width: 70% !important;
    margin: 0 auto !important;
}
'''

with gr.Blocks(theme=theme, css=css) as interface:
    model_dict = gr.State(start_model_dict)
    support_system_role = gr.State(start_support_system_role)
    
    # ================= CHAT BOT PAGE ======================
    with gr.Tab('Chatbot'):
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    type='messages',  # new in gradio 5+
                    show_copy_button=True, 
                    bubble_full_width=False, 
                    height=480,
                    )
                user_message = gr.Textbox(label='User')

                with gr.Row():
                    user_message_btn = gr.Button('Send')
                    stop_btn = gr.Button('Stop')
                    clear_btn = gr.Button('Clear')

                system_prompt = get_system_prompt_component(interactive=support_system_role.value)

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
                        generate_args = get_generate_args(do_sample.value)
                        do_sample.change(
                            fn=get_generate_args,
                            inputs=do_sample,
                            outputs=generate_args,
                            show_progress=False,
                        )

        generate_event = gr.on(
            triggers=[user_message.submit, user_message_btn.click],
            fn=user_message_to_chatbot,
            inputs=[user_message, chatbot],
            outputs=[user_message, chatbot],
        ).then(
            fn=bot_response_to_chatbot,
            inputs=[chatbot, model_dict, system_prompt, support_system_role, history_len, do_sample, *generate_args],
            outputs=[chatbot],
        )
        stop_btn.click(
            fn=None,
            inputs=None,
            outputs=None,
            cancels=generate_event,
        )
        clear_btn.click(
            fn=lambda: None,
            inputs=None,
            outputs=[chatbot],
            )

    # ================= LOAD MODELS PAGE ======================
    with gr.Tab('Load model'):
        gguf_url = gr.Textbox(
            value='',
            label='Link to GGUF',
            placeholder='URL link to the model in GGUF format',
            )
        load_model_btn = gr.Button('Downloading GGUF and initializing model')
        load_log = gr.Textbox(
            value=start_load_log,
            label='Model loading status',
            lines=3,
            )
            
        load_model_btn.click(
            fn=download_gguf_and_init_model,
            inputs=[gguf_url, model_dict],
            outputs=[model_dict, support_system_role, load_log],
        ).success(
            fn=get_system_prompt_component,
            inputs=[support_system_role],
            outputs=[system_prompt],
        )

        gr.HTML("""<h3 style='text-align: center'>
        <a href="https://github.com/sergey21000/gradio-llamacpp-chatbot" target='_blank'>GitHub Repository</a></h3>
        """)

if __name__ == '__main__':
    interface.launch(server_name='0.0.0.0', server_port=7860)