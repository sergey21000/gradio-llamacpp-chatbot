from typing import Iterator


CHAT_HISTORY = list[dict[str, str | list]]


def test_chatbot_with_user_message(chatbot_with_user_message):
    print(f'Chatbot with user message: {chatbot_with_user_message}')
    assert len(chatbot_with_user_message) == 1, 'The message was not added to the chat'
    message = chatbot_with_user_message[0]
    assert isinstance(message, dict)
    assert message['role'] == 'user'
    assert isinstance(message['content'], list)
    assert len(message['content']) == 2
    assert message['content'][0].get('path', '').endswith('белка.png')


def test_llm_pipepline(chatbot_with_user_message, config):
    from modules.ui_fn import UiFn

    stream_chatbot: Iterator[CHAT_HISTORY] = UiFn.llm_response_to_chatbot(
        chatbot=chatbot_with_user_message,
        config=config,
    )
    for result_chatbot in stream_chatbot:
        pass
    assistant_message = result_chatbot[-1]
    print(f'Chatbot response: {assistant_message}')
    assert isinstance(assistant_message, dict)
    assert assistant_message['role'] == 'user'
    assert isinstance(assistant_message['content'], list)
    assert len(assistant_message['content']), 'LLM did not respond'
    