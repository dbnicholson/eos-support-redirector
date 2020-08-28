FROM python:3-slim

RUN apt-get update && \
    apt-get -y install curl && \
    apt-get clean
RUN pip install --no-cache-dir gunicorn

WORKDIR /app
COPY redirector.py .
COPY run .

USER nobody
EXPOSE 8000
ENV WORKERS=2
CMD ["./run"]
HEALTHCHECK CMD ["curl", "-sS", "-A", "healthcheck", "http://127.0.0.1:8000"]
