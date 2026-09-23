FROM python:3.12-slim

# Install system dependencies for audio (limited in Docker)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    flac \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml requirements.txt ./
COPY src/ ./src/
COPY README.md LICENSE ./

# Install the package
RUN pip install --no-cache-dir -e .

# Create data directory
RUN mkdir -p /app/data

# Set environment defaults
ENV JARVIS_TTS_ENABLED=false
ENV JARVIS_VOICE_INPUT_ENABLED=false
ENV JARVIS_LOG_LEVEL=INFO
ENV JARVIS_DATA_DIR=/app/data

# Note: Voice features (TTS, speech recognition) are disabled by default in Docker.
# To use Jarvis in Docker, interact via text input only.
# Set JARVIS_LLM_API_KEY environment variable to enable LLM conversation.

ENTRYPOINT ["python", "-m", "jarvis"]
