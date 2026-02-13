FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc  \
    libpq-dev  \
    curl  \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY init_entrypoint.sh .
RUN chmod +x init_entrypoint.sh

ENTRYPOINT ["/bin/sh", "/app/init_entrypoint.sh"]
CMD []