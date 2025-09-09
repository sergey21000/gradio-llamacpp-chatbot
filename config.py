import os


GENERATION_KWARGS = dict(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    repeat_penalty=1.0,
)

LLAMA_MODEL_KWARGS = dict(
    repo_id=os.getenv('REPO_ID', 'bartowski/google_gemma-3-1b-it-GGUF'),
    filename=os.getenv('FILENAME', 'google_gemma-3-1b-it-Q8_0.gguf'),
    # repo_id=os.getenv('REPO_ID', 'bartowski/Qwen_Qwen3-0.6B-GGUF'),
    # filename=os.getenv('FILENAME', 'Qwen_Qwen3-0.6B-Q4_K_M.gguf'),
    local_dir=os.getenv('LOCAL_DIR', 'model'),
    cache_dir=os.getenv('LOCAL_DIR', 'model'),
    n_gpu_layers=-1,
    verbose=True,
    n_ctx=4096,
)

SHOW_THINKING = False
