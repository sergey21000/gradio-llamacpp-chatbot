FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim
ENV UV_SYSTEM_PYTHON=1

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY modules modules
COPY app.py config.py .

ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860
CMD ["uv", "run", "app.py"]