FROM debian:latest

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

RUN apt-get -y update
RUN apt-get -y install socat wget build-essential unzip

RUN mkdir -p /ctf

WORKDIR /ctf
RUN wget http://www.lua.org/ftp/lua-5.4.4.tar.gz
RUN tar zxpf lua-5.4.4.tar.gz
WORKDIR /ctf/lua-5.4.4
RUN make all test
RUN make install

WORKDIR /ctf
RUN wget https://luarocks.org/releases/luarocks-3.8.0.tar.gz
RUN tar zxpf luarocks-3.8.0.tar.gz
WORKDIR /ctf/luarocks-3.8.0
RUN ./configure
RUN make install

RUN luarocks install luafilesystem

WORKDIR /ctf
COPY main.lua .

COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-`cat /flag.txt | md5sum | awk -F ' ' '{print $1}' | tr -d '\n'`.txt

USER ctf
EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'lua main.lua'