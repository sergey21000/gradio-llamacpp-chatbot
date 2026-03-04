import pytest


@pytest.fixture(scope='session', autouse=True)
def env() -> None:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='tests/.test.env')


@pytest.fixture(scope='session')
def config():
    from config import Config

    config = Config()
    config.generation_kwargs['enable_thinking'] = True
    config.generation_kwargs['show_thinking'] = True
    return config


@pytest.fixture(scope='session')
def chatbot_with_user_message():
    from modules.ui_fn import UiFn

    chatbot = []
    user_message = {
        'text': 'Что на картинке?',
        'files': ['tests/белка.png'],
    }
    user_msg, updated_chatbot = UiFn.user_message_to_chatbot(
        user_message=user_message,
        chatbot=chatbot,
    )
    return updated_chatbot
