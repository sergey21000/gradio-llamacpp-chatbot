FROM nvcr.io/nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04 AS builder

RUN apt-get update && apt-get install -y \
	python3 python3-pip git \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements-base.txt requirements/requirements-cuda.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements-cuda.txt

FROM nvcr.io/nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
	python3 python3-pip \
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
