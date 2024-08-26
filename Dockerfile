# Bissmillahirrahmanirraheem

FROM python:3.10

ARG GPG_PRIVATE_KEY_PART_1
ARG GPG_PRIVATE_KEY_PART_2

ENV GPG_PRIVATE_KEY_PART_1=${GPG_PRIVATE_KEY_PART_1}
ENV GPG_PRIVATE_KEY_PART_2=${GPG_PRIVATE_KEY_PART_2}
ENV ENVIRONMENT="PRODUCTION"

ENV GPG_TTY=/dev/console

ENV PYTHONUNBUFFERED="TRUE"
ENV PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    gpg \
    nano \
    wget && \
    sh -c "echo 'deb https://gitsecret.jfrog.io/artifactory/git-secret-deb git-secret main' >> /etc/apt/sources.list" \
    && wget -qO - 'https://gitsecret.jfrog.io/artifactory/api/gpg/key/public' | apt-key add - && \
    apt-get update && apt-get install -y --no-install-recommends git-secret wkhtmltopdf


# Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .
RUN echo $GPG_PRIVATE_KEY_PART_1$GPG_PRIVATE_KEY_PART_2 | tr -d "\n" | base64 -d | gpg --import - && git secret reveal

# RUN gpg --import GPG_PRIVATE_KEY && git init && git secret reveal
# RUN echo "hello world" && echo $LOGFIRE_TOKEN

RUN pip install --no-cache-dir -r requirements.txt

RUN alembic upgrade head && python initialize.py

CMD uvicorn app.main:app --port $PORT --host 0.0.0.0
