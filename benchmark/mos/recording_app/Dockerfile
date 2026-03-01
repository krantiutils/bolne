FROM python:3.12-slim

WORKDIR /app

COPY recording_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY recording_app/server.py .
COPY recording_app/templates/ templates/
COPY sentences.json /app/sentences.json

ENV SENTENCES_PATH=/app/sentences.json
ENV ADMIN_PASSWORD=changeme

VOLUME /app/data

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
