FROM python:3.11.6

WORKDIR /app
COPY . .

RUN pip3 install -r /app/requirements.txt

RUN rm -rf /app/.git
RUN rm /app/.gitignore
RUN rm /app/requirements.txt