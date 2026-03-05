FROM ghcr.io/sergey21000/gradio-llamacpp-chatbot:main-hf

RUN useradd -m -u 1000 user \
    && chown -R user:user /app

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app
COPY --chown=user .settings.env ./

CMD ["uv", "run", "app.py"]