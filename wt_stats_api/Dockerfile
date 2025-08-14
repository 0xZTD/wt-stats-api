FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg2 \
        xvfb \
        chromium \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate non-root user for better security
RUN useradd -m appuser
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (as non-root)
USER appuser
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (as non-root)
COPY --chown=appuser . wt_stats_api/
EXPOSE 8650

CMD [ "python","-m", "uvicorn","wt_stats_api.main:app","--host","0.0.0.0","--port","8650" ]
