import os

from llama_cpp_py import (
    LlamaReleaseManager,
    LlamaSyncServer,
    LlamaSyncClient,
)

from config import Config


openai_base_url = os.getenv('OPENAI_BASE_URL', '')
openai_api_key = os.getenv('OPENAI_API_KEY', '')
openai_model = os.getenv('OPENAI_MODEL', '')

if openai_api_key or openai_base_url:
    llama_server = None
    llm_client = LlamaSyncClient(
        openai_base_url=openai_base_url,
        api_key=openai_api_key,
        model=openai_model,
    )
else:
    priority_patterns = ['cuda'] if Config.LLAMACPP_PREFER_CUDA_BUILD else ['cpu']
    llama_server = LlamaSyncServer(
        verbose=True,
        release_manager=LlamaReleaseManager(
            tag=Config.LLAMACPP_RELEASE_TAG,
            priority_patterns=priority_patterns,
        ),
    )
    llm_client = LlamaSyncClient(openai_base_url=llama_server.openai_base_url)
