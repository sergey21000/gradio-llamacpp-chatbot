FROM python:3.12-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY modules modules
COPY app.py config.py .

ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860
CMD ["python3", "app.py"]