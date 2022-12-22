FROM debian:latest

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip install -r /var/www/apache-flask/app/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers

# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

COPY ./run.py /var/www/apache-flask/run.py
COPY ./app /var/www/apache-flask/app/

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log


EXPOSE 80

WORKDIR /var/www/apache-flask

RUN chmod 777 app/static/uploads/

CMD  /usr/sbin/apache2ctl -D FOREGROUND
