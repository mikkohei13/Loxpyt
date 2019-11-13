
FROM tiangolo/uwsgi-nginx-flask:python3.7

# Add tools
RUN apt-get update && \
apt-get -y install libimage-exiftool-perl ffmpeg

# Add pip modules
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Add app as the last step (invalidates cache)
COPY ./app /app
