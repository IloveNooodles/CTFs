FROM php:7.4-fpm

RUN apt-get update && apt-get install -y \
    libmagickwand-dev \
    libmagickcore-dev

RUN pecl install imagick-3.7.0 && docker-php-ext-enable imagick

COPY web/. /var/www/html
COPY flag.txt /flag.txt

RUN chmod 444 /flag.txt
RUN chown -R root:root /var/www/html
RUN chmod -R a-w /var/www/html/
RUN chmod 777 /var/www/html/results
RUN chown root:root /var/www/html/results

EXPOSE 9000
CMD ["php-fpm"]