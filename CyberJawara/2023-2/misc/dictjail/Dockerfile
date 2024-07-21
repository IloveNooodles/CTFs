FROM ubuntu:22.04

RUN apt-get -y update && apt-get -y install socat gcc python3 less --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/chall
RUN groupadd ctf && useradd --no-create-home -g ctf ctf

COPY dictjail.py dictjail.py
COPY flag.txt /flag.txt
COPY readflag /readflag

RUN chmod u+s /readflag 
RUN chmod 400 /flag.txt

ENV TERM=xterm

EXPOSE 5000
ENTRYPOINT socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"./dictjail.py",su=ctf,pty,stderr
