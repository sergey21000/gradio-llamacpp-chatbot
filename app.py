import os
import pprint

from dotenv import load_dotenv
load_dotenv()
load_dotenv(dotenv_path='.settings.env')

from modules.logger import logger
from modules.ui_create import demo
from modules.llm import llama_server, llm_client
from config import UiGradioConfig


if __name__ == '__main__':
    RUNNING_IN_DOCKER = os.getenv('RUNNING_IN_DOCKER', '0').lower() in ('1', 'true')
    try:
        if not RUNNING_IN_DOCKER and llama_server:
            llama_server.start()
            logger.debug((
                'llama.cpp server started, props: '
                f'{pprint.pformat(llm_client.get_props())}'
            ))
        demo.launch(**UiGradioConfig.get_demo_launch_kwargs())
    finally:
        if not RUNNING_IN_DOCKER and llama_server:
            llama_server.stop()
        demo.close()
