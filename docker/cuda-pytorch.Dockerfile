FROM pytorch/pytorch:2.10.0-cuda13.0-cudnn9-devel AS builder

RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements-base.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements-base.txt \
	--extra-index-url https://download.pytorch.org/whl/cu130


FROM pytorch/pytorch:2.10.0-cuda13.0-cudnn9-runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
	libmagic-dev \
	poppler-utils \
	libgl1 libglib2.0-0 \
	# tesseract-ocr \
	# tesseract-ocr-rus \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --break-system-packages /wheels/* && rm -rf /wheels

WORKDIR /app
COPY modules modules
COPY app.py config.py .

EXPOSE 7860
CMD ["python3", "app.py"]
