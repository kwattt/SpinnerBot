FROM python:3.9-alpine

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISCORD_TOKEN=changeme
ENV DISCORD_PREFIX=!
CMD [ "python", "./spinner.py" ]
