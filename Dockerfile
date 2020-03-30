FROM ubuntu:focal

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-psycopg2 \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*

# Due to https://github.com/pypa/pip/issues/5599
RUN python3 -m pip install --upgrade pip

COPY . /app/btools
RUN mkdir -p /app/pip_cache_dir
WORKDIR /app/btools

RUN pip3 install -r requirements.txt

# Run Application

ENV BTOOLS_PORT 8000
ENV BTOOLS_DATABASE_HOST 10.224.105.13
ENV BTOOS_DATABASE btools
ENV BTOOLS_DATABASE_USER telescreen
ENV BTOOLS_DATABASE_PASSWORD telescreen

EXPOSE 8080
CMD python3 manage.py runserver 0:8080
