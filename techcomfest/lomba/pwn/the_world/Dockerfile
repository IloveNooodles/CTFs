FROM ubuntu

RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get install -y nano apache2 apache2-utils \ 
    gcc gcc-multilib g++ g++-multilib build-essential \
    libc6:i386 libncurses5:i386 libstdc++6:i386 libseccomp-dev

WORKDIR /var/www/html

COPY robots.txt .
COPY Dockerfile .

COPY main.c .
RUN gcc -o main -fno-stack-protector -z execstack -no-pie main.c -lseccomp
RUN rm -f main.c
RUN cp main pwny.cgi

COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-`cat /flag.txt | md5sum | awk -F ' ' '{print $1}' | tr -d '\n'`.txt

RUN a2enmod cgi
COPY 000-default.conf /etc/apache2/sites-available

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]