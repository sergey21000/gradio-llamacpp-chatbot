FROM python:3.12 AS builder

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY --chown=user app.py utils.py init_model.py config.py .
ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860
CMD ["python3", "app.py"]