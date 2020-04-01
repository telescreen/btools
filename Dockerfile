FROM ubuntu:focal

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-psycopg2 \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 -s /bin/bash ubuntu
ENV PATH="/home/ubuntu/.local/bin:${PATH}"
# Due to https://github.com/pypa/pip/issues/5599
RUN python3 -m pip install --upgrade pip

USER ubuntu
COPY --chown=ubuntu:ubuntu . /home/ubuntu/btools
WORKDIR /home/ubuntu/btools
RUN mkdir -p /home/ubuntu/btools/pip_cache_dir
RUN python3 -m pip install -r requirements.txt --cache-dir /home/ubuntu/btools/pip_cache_dir
# Run Application
EXPOSE 8080
CMD python3 manage.py runserver 0:8080
