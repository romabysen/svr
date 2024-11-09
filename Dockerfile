FROM python:3.12-alpine AS builder
RUN pip install -U pdm
RUN mkdir /code
WORKDIR /code
ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock /code/
RUN pdm install --check --prod --no-editable

FROM python:3.12-alpine
RUN apk add --no-cache tini
COPY . /code/
COPY --from=builder /code/.venv/ /code/.venv
ENTRYPOINT ["/sbin/tini", "--"]
WORKDIR /code
CMD [\
    ".venv/bin/hypercorn",\
    "svr.app",\
    "-b 0.0.0.0:${PORT}"\
]
