FROM python:3.12-alpine
RUN apk add --no-cache tini && pip install --root-user-action=ignore pdm
RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pdm export > requirements.txt && pip install --root-user-action=ignore -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["hypercorn", "-c", "file:deploy/quart.py", "svr.app"]
