FROM python:3.9-alpine

RUN python3 -m pip install requests ping3

WORKDIR /usr/local/routerwatchdog

COPY . .
