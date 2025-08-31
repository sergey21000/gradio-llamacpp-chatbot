GENERATION_KWARGS = dict(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    repeat_penalty=1.0,
)

LLAMA_MODEL_KWARGS = dict(
    repo_id='bartowski/google_gemma-3-1b-it-GGUF',
    filename='google_gemma-3-1b-it-Q8_0.gguf',
    # repo_id='bartowski/Qwen_Qwen3-0.6B-GGUF',
    # filename='Qwen_Qwen3-0.6B-Q4_K_M.gguf',
    local_dir='model',
    cache_dir='model',
    n_gpu_layers=-1,
    verbose=True,
    n_ctx=4096,
)

SHOW_THINKING = False