import gradio as gr

from config import Config


class UiComponents:
    def __init__(self):
        KW = Config().generation_kwargs
        self.chatbot = gr.Chatbot(
            sanitize_html=False,
            render=False,
            # buttons=['copy', 'copy_all', 'share'],
            # height=480,
            # api_visibility='public',  # 'private'
        )
        self.user_msg = gr.MultimodalTextbox(
            interactive=True,
            file_count='single',
            placeholder='Enter a message or attach a file',
            sources=['upload'],  # ['upload', 'microphone']
            # show_label=False,
            render=False,
        )
        self.user_msg_btn = gr.Button('Send', render=False)
        self.stop_btn = gr.Button('Stop', render=False)
        self.clear_btn = gr.Button('Clear', render=False)
        if Config.SUPPORT_SYSTEM_ROLE:
            self.system_prompt = gr.Textbox(
                value=KW['system_prompt'],
                label='Edit system prompt',
                interactive=True,
                render=False,
            )
        else:
            self.system_prompt = gr.Textbox(
                value='System prompt is not supported by this model',
                label='Edit system prompt',
                interactive=False,
                render=False,
            )
        self.history_len = gr.Slider(
            minimum=0,
            maximum=10,
            value=KW['history_len'],
            step=1,
            info='Number of previous user-bot message pairs to keep in chat history',
            label='history len',
            show_label=False,
            render=False,
        )
        self.do_sample = gr.Checkbox(
            value=KW['do_sample'],
            label='do_sample',
            info='Activate random sampling',
            render=False,
        )
        self.temperature = gr.Slider(
            minimum=0.1,
            maximum=3,
            value=KW['temperature'],
            step=0.1,
            label='temperature',
            visible=KW['do_sample'],
            render=False,
        )
        self.top_p = gr.Slider(
            minimum=0,
            maximum=1,
            value=KW['top_p'],
            step=0.01,
            label='top_p',
            visible=KW['do_sample'],
            render=False,
        )
        self.top_k = gr.Slider(
            minimum=1,
            maximum=50,
            value=KW['top_k'],
            step=1,
            label='top_k',
            visible=KW['do_sample'],
            render=False,
        )
        self.repeat_penalty = gr.Slider(
            minimum=1,
            maximum=5,
            value=KW['repeat_penalty'],
            step=0.1,
            label='repeat_penalty',
            visible=KW['do_sample'],
            render=False,
        )
        self.max_output_tokens = gr.Slider(
            minimum=-1,
            maximum=4096,
            value=KW['max_output_tokens'],
            step=6,
            label='max_output_tokens',
            render=False,
        )
        self.enable_thinking = gr.Checkbox(
            value=False,
            label='Enable thinking',
            show_label=False,
            visible=True,
            render=False,
        )
        self.show_thinking = gr.Checkbox(
            value=False,
            label='Show thinking',
            show_label=False,
            visible=True,
            render=False,
        )

    def get_sampling_components(self) -> list[gr.Component]:
        return [
            self.temperature,
            self.top_p,
            self.top_k,
            self.repeat_penalty,
        ]

    @staticmethod
    def update_visibility(
        visible: bool,
        num_componets: int,
    ) -> dict | list[dict]:
        if num_componets == 1:
            return gr.update(visible=visible)
        return [gr.update(visible=visible) for _ in range(num_componets)]

    def update_config(self, config: Config, *components: list[gr.Component]) -> None:
        for i, key in enumerate(config.generation_kwargs):
            config.generation_kwargs[key] = components[i]

    def get_generation_components(self, config: Config) -> list[gr.Component]:
        components = []
        for key in config.generation_kwargs:
            components.append(self.__dict__[key])
        return components
