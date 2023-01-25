FROM --platform=linux/amd64 ghcr.io/snwflake/python-poetry-alpine:latest

ENV PIP_DISABLE_PIP_VERSION_CHECK   1
ENV PYTHONDONTWRITEBYTECODE         1
ENV PYTHONUNBUFFERED                1

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry install --without dev

COPY . .

ENTRYPOINT [ "poetry" ]
CMD [ "run", "python", "main.py" ]