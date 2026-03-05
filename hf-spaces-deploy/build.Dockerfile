FROM ghcr.io/sergey21000/gradio-llamacpp-chatbot:main

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ggerganov/llama.cpp /opt/llama.cpp && \
    cd /opt/llama.cpp && \
    cmake -S . -B build \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_BUILD_SERVER=ON \
      -DLLAMA_BUILD_TESTS=OFF \
      -DGGML_NATIVE=OFF \
      -DGGML_CPU_ALL_VARIANTS=ON \
      -DGGML_BACKEND_DL=ON \
      -DLLAMA_CUBLAS=OFF \
      -DLLAMA_VULKAN=OFF \
      -DLLAMA_SYCL=OFF && \
    cmake --build build --config Release -j$(nproc)

ENV PATH=/opt/llama.cpp/build/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/llama.cpp/build/bin:$LD_LIBRARY_PATH
ENV LLAMACPP_DIR=/opt/llama.cpp/build/bin

WORKDIR /app

CMD ["uv", "run", "app.py"]