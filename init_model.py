from llama_cpp import Llama
from config import LLAMA_MODEL_KWARGS


MODEL = Llama.from_pretrained(**LLAMA_MODEL_KWARGS)
SUPPORT_SYSTEM_ROLE = 'System role not supported' not in MODEL.metadata['tokenizer.chat_template']
