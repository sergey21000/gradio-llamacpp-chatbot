

---
# Gradio llama-cpp-python Chatbot

<div align="left">
<a href="https://huggingface.co/spaces/sergey21000/gradio-llamacpp-chatbot"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow" alt="Hugging Face Spaces"></a>
<a href="https://hub.docker.com/r/sergey21000/gradio-llamacpp-chatbot"><img src="https://img.shields.io/badge/Docker-Hub-blue?logo=docker" alt="Docker Hub "></a>
</div>

Чат-бот на `llama-cpp-python` с веб-интерфейсом на `Gradio`


---
## 📋 Содержание

- 📽 [Демонстрация](#-Демонстрация)
- 🖼 [Скриншоты](#-Скриншоты)
- 🚀 [Функционал](#-Функционал)
- 🏗 [Стек технологий](#-Стек-технологий)
- 🐍 [Установка и запуск через Python](#-Установка-и-запуск-через-Python)
- 🐳 [Установка и запуск через Docker](#-Установка-и-запуск-через-Docker)
  - 🏃‍ [Запуск контейнера из образа Docker HUB](#-Запуск-контейнера-из-образа-Docker-HUB)
  - 🏗️ [Сборка своего образа и запуск контейнера](#-Сборка-своего-образа-и-запуск-контейнера)
- 📱 [Установка и запуск на Android](#-Установка-и-Запуск-на-Android)


---
## 📽 Демонстрация

В Google Colab <a href="https://colab.research.google.com/drive/1tClehCQILXLSXYqIZII569S1eTWnf8hZ"><img src="https://img.shields.io/static/v1?message=Open%20in%20Colab&logo=googlecolab&labelColor=5c5c5c&color=0f80c1&label=%20" alt="Open in Colab"></a> ноутбуке дополнительно реализовано:  
 - Код приложения с комментариями
 - Демонстрация пошагового инференса моделей через `llama-cpp-python`
 - Пример деплоя веб-приложения на фреймворке Gradio на облачный сервер
 - Подключение и настройка сервера NGINX 
 - Регистрация домена для своего сайта
 - Установка SSL сертификатов для работы приложения по протоколу HTTPS на своем сайте


---
## 🖼 Скриншоты

<details>
<summary>Главная страница приложения</summary>

![Главная страница](./screenshots/main_page.png)
</details>


---
## 🚀 Функционал

- Генерация ответа с использованием моделей в формате GGUF
- Настройка параметров генерации (`temperature`, `top_k`, `top_p`, `repetition_penalty`)
- Возможность указать системный промт (если модель его не поддерживает это будет отображено)
- Выбор количества учитываемых сообщений в истории при подаче промта в модель
- Возможность выбора моделей в формате GGUF перед запуском

После запуска приложения происходит загрузка LLM модели по умолчанию (`google_gemma-3-1b-it-Q8_0.gguf`, 1 GB) в папку `./models`  
Изменить LLM модель перед запуском приложения можно в файле `config.py`, для необходимо заменить название репозитория и название файла модели в формате GGUF 

Где искать LLM модели в формате GGUF
- [bartowski](https://huggingface.co/bartowski) 
- [mradermacher](https://huggingface.co/mradermacher) 
- [Поиск на HuggingFace](https://huggingface.co/models?pipeline_tag=text-generation&library=gguf&sort=trending)


---
## 🏗 Технологии

- [python](https://www.python.org/) >= 3.10
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) для инференса моделей в формате GGUF
- [gradio](https://github.com/gradio-app/gradio) для написания веб-интерфейса
- [Модель gemma-3-1b](https://huggingface.co/bartowski/google_gemma-3-1b-it-GGUF) `google_gemma-3-1b-it-Q8_0.gguf` в формате GGUF в качестве LLM модели по умолчанию


Работоспособность приложения проверялась на следующих ОС и версиях Python
- Ubuntu 22.04, python 3.11, CUDA 12.5 (Google Colab)
- Windows 10, python 3.12, CUDA 12.8
- Android 11 (MIUI 12), Termux, python 3.12
- Android 11 (MIUI 12), Ubuntu 22.04 (Andronix), python 3.10


---
## 🐍 Установка и запуск через Python

**1) Клонирование репозитория**  

```
git clone https://github.com/sergey21000/gradio-llamacpp-chatbot.git
cd gradio-llamacpp-chatbot
```

**2) Создание и активация виртуального окружения (опционально)**

- *Linux*
  ```
  python3 -m venv env
  source env/bin/activate
  ```

- *Windows CMD*
  ```
  python -m venv env
  env\Scripts\activate
  ```

- *Windows PowerShell*
  ```
  python -m venv env
  env\Scripts\activate.ps1
  ```

**3) Установка llama-cpp-python**  

- *С поддержкой CPU*
  ```
  pip install llama-cpp-python
  ```

- *С поддержкой CUDA*
  - Linux
    ```
    CMAKE_ARGS="-DGGML_CUDA=on pip install llama-cpp-python
    ```
  - Windows CMD
    ```
    set CMAKE_ARGS=-DGGML_CUDA=on
	pip install llama-cpp-python
    ```

> [!NOTE]
> Для установки `llama-cpp-python` на Windows с поддержкой CUDA необходимо установить [Visual Studio 2022 Community](https://visualstudio.microsoft.com/ru/downloads/) и [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive), как например показано в [этой](https://github.com/abetlen/llama-cpp-python/discussions/871#discussion-5812096) или [этой](https://github.com/Granddyser/windows-llama-cpp-python-cuda-guide?tab=readme-ov-file#12-visual-studio-2019-installation-and-configuration) инструкциях

Для более быстрой установки можно воспользоваться готовыми колесами, например [отсюда](https://github.com/sergey21000/llama-cpp-python-wheels?tab=readme-ov-file#installation-examples) или [отсюда](https://github.com/abetlen/llama-cpp-python/releases)  
Например установка на *Linux x86_64 / Python 3.12 с поддержкой CUDA 12.9*
```
pip install https://github.com/sergey21000/llama-cpp-python-wheels/releases/download/v0.3.14/llama_cpp_python-0.3.14-cp312-cp312-linux_x86_64.cu129.whl
```

**5) Установка Gradio**  

Установка Gradio и прочих зависимостей
```
pip install -r requirements-base.txt
```

**5) Запуск сервера Gradio**  

```
python3 app.py
```
После запуска сервера перейти в браузере по адресу http://127.0.0.1:7860/  
Приложение будет доступно через некоторое время (после первоначальной загрузки модели в директорию `./models`)


---
## 🐳 Установка и запуск через Docker

> [!NOTE]  
Для запуска приложения с поддержкой GPU CUDA необходима установка [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).


### 🏃 Запуск контейнера из образа Docker HUB

- *С поддержкой CPU*
  ```
  docker run -it -p 7860:7860 \
	-v ./model:/app/model \
	sergey21000/gradio-llamacpp-chatbot:cpu-v1.0
  ```

- *С поддержкой CUDA*
  ```
  docker run -it --gpus all -p 7860:7860 \
	-v ./model:/app/model \
	sergey21000/gradio-llamacpp-chatbot:nvidia-cuda12.9-v1.0
  ```


### 🏗️ Сборка своего образа и запуск контейнера

**1) Клонирование репозитория**  
```bash
git clone https://github.com/sergey21000/gradio-llamacpp-chatbot.git
cd gradio-llamacpp-chatbot
```

**2) Сборка образа и запуск контейнера**

- *С поддержкой CPU*  

  Сборка образа
  ```
  docker build -t gradio-llamacpp-chatbot:cpu-v1.0 -f Dockerfile-cpu .
  ```
  Запуск контейнера
  ```
  docker run -it -p 7860:7860 -v ./model:/app/model gradio-llamacpp-chatbot:cpu-v1.0
  ```

- *С поддержкой CUDA*  

  Сборка образа на основе образа Nvidia
  ```
  docker build -t gradio-llamacpp-chatbot:nvidia-cuda12.9-v1.0 -f Dockerfile-cuda-nvidia .
  ```
  Запуск контейнера
  ```
  docker run -it --gpus all -p 7860:7860 \
	-v ./model:/app/model \
	gradio-llamacpp-chatbot:nvidia-cuda12.9-v1.0
  ```
  
После запуска сервера перейти в браузере по адресу http://127.0.0.1:7860/  
Приложение будет доступно после первоначальной загрузки модели в директорию `./models`

---
Приложение создавалось для тестирования LLM моделей как любительский проект  
Оно написано для демонстрационных и образовательных целей и не предназначалось / не тестировалось для промышленного использования


## 📱 Установка и запуск на Android

[Инструкции](https://github.com/sergey21000/gradio-llamacpp-chatbot/blob/main/README_Android.md) по запуску бота на Android


## Лицензия

Этот проект лицензирован на условиях лицензии [MIT](./LICENSE).
