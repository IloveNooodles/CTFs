FROM denoland/deno:latest

RUN mkdir -p /ctf
WORKDIR /ctf
COPY . .

RUN chmod 444 flag.txt

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

RUN dpkg --add-architecture i386
RUN apt-get -y update
RUN apt-get -y install socat

RUN deno cache main.ts

USER ctf
EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'deno run --no-prompt --allow-read main.ts'