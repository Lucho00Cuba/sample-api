FROM docker.io/python:3.12-alpine as build

RUN apk add --no-cache gcc python3-dev musl-dev linux-headers make bash && \
    python3 -m ensurepip

WORKDIR /build

COPY . .

RUN make dependencies && \
    make tests

FROM docker.io/python:3.12-alpine

ARG BUILD_DATE
ARG ENVIRONMENT

LABEL maintainer="lomv0209@gmail.com" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/Lucho00Cuba/sample-api.git"

ENV ENVIRONMENT=$ENVIRONMENT:PROD

WORKDIR /opt

COPY src/ /opt/
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

CMD ["/opt/entrypoint.sh"]