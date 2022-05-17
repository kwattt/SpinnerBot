## running locally


1. install docker https://docs.docker.com/engine/install/ubuntu/#installation-methods
2. git clone https://github.com/kwattt/SpinnerBot
3. create the data.json file
4. adjust info.json
5. in repo folder run `docker build -t spinnerbot .`
6. then run `docker run spinnerbot:latest` or `docker run -d spinnerbot:latest` for detached running.
7. done!