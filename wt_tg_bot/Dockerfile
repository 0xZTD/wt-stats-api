FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt .

USER appuser
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
