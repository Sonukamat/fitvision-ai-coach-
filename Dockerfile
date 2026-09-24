FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libegl1 \
    libgles2 \
    libopengl0 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir \
    streamlit \
    streamlit-webrtc \
    mediapipe \
    "numpy<2.0.0" \
    pandas \
    groq \
    gTTS \
    python-dotenv

EXPOSE 7860

CMD ["streamlit", "run", "Main App/main.py", "--server.port=7860", "--server.address=0.0.0.0"]
