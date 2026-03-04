import gradio as gr

from config import Config, UiGradioConfig
from modules.ui_fn import UiFn
from modules.ui_components import UiComponents


# CONF = Config()
demo = gr.Blocks(**UiGradioConfig.get_demo_blocks_kwargs())


with demo:
    CONF = Config()
    config = gr.State(Config())
    ui = UiComponents()
    with gr.Row():
        with gr.Column(scale=3):
            ui.chatbot.render()
            ui.user_msg.render()
            with gr.Accordion('Prompt', open=False):
                ui.system_prompt.render()

        with gr.Column(scale=1, min_width=80):
            with gr.Group():
                gr.Markdown('Length of message history')
                ui.history_len.render()
                with gr.Group():
                    gr.Markdown('LLM thinking')
                    ui.enable_thinking.render()
                    ui.show_thinking.render()
                with gr.Group():
                    gr.Markdown('Generation parameters')
                    ui.max_output_tokens.render()
                    ui.do_sample.render()
                    ui.temperature.render()
                    ui.top_p.render()
                    ui.top_k.render()
                    ui.repeat_penalty.render()

    ui.do_sample.change(
        fn=lambda visible: UiComponents.update_visibility(
            visible=visible,
            num_componets=len(ui.get_sampling_components()),
        ),
        inputs=ui.do_sample,
        outputs=ui.get_sampling_components(),
        show_progress=False,
    )

    generation_components = ui.get_generation_components(CONF)
    ui.user_msg.submit(
        fn=UiFn.user_message_to_chatbot,
        inputs=[ui.user_msg, ui.chatbot],
        outputs=[ui.user_msg, ui.chatbot],
    ).then(
        fn=ui.update_config,
        inputs=[config, *generation_components],
        outputs=None,
    ).then(
        fn=UiFn.llm_response_to_chatbot,
        inputs=[ui.chatbot, config],
        outputs=ui.chatbot,
    )

    # generate_event = gr.on(
    #     triggers=[ui.user_msg.submit],
    #     fn=UiFn.user_message_to_chatbot,
    #     inputs=[ui.user_msg, ui.chatbot],
    #     outputs=[ui.user_msg, ui.chatbot],
    # ).then(
    #     fn=UiFn.llm_response_to_chatbot,
    #     inputs=[
    #         ui.chatbot,
    #         ui.system_prompt,
    #         ui.history_len,
    #         ui.max_output_tokens,
    #         ui.enable_thinking,
    #         ui.show_thinking,
    #         ui.do_sample,
    #         ui.temperature,
    #         ui.top_p,
    #         ui.top_k,
    #         ui.repeat_penalty,
    #     ],
    #     outputs=[ui.chatbot],
    # )

