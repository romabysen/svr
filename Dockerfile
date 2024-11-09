FROM python:3.12-alpine
RUN apk add --no-cache tini && pip install --root-user-action=ignore pdm
RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pdm install --check --prod --no-editable

ENTRYPOINT ["/sbin/tini", "--"]
CMD [".venv/bin/hypercorn", "-c", "file:deploy/quart.py", "svr.app"]
