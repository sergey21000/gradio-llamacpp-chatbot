import os

GENERATION_KWARGS = dict(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    repeat_penalty=1.0,
)

LLAMA_MODEL_KWARGS = dict(
    repo_id=os.getenv('REPO_ID', 'bartowski/Qwen_Qwen3-0.6B-GGUF'),
    filename=os.getenv('FILENAME', 'Qwen_Qwen3-0.6B-Q4_K_M.gguf'),
    local_dir=os.getenv('LOCAL_DIR', 'model'),
    verbose=False,
)

SHOW_THINKING = True
