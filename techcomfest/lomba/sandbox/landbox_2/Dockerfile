FROM debian:latest

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

RUN apt-get -y update
RUN apt-get -y install lua5.4
RUN apt-get -y install socat

RUN mkdir -p /ctf
WORKDIR /ctf
COPY main.lua .

COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-`cat /flag.txt | md5sum | awk -F ' ' '{print $1}' | tr -d '\n'`.txt

USER ctf
EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork 'EXEC:lua main.lua'