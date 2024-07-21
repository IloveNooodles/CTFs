FROM php:8-cli-alpine

RUN apk add --no-cache curl  

RUN apk add --no-cache make

# Install WP-CLI in the toolbox
RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar  
RUN chmod +x wp-cli.phar  
RUN mv wp-cli.phar /usr/local/bin/wp-cli

# Install MySQL extension, as WP-CLI needs to access to WordPress database
RUN apk update && \
    apk add mysql-client

# Install dockerize
RUN apk add --no-cache openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# Add Makefile to scripts dir
ADD Makefile /scripts/Makefile

RUN docker-php-ext-install mysqli

ENTRYPOINT [ "make", "-f", "/scripts/Makefile" ]  

