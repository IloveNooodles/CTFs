FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD ./pwn.xinetd  /etc/xinetd.d/pwn
ADD ./init.sh     /etc/init.sh
ADD ./redir.sh    /home/pwn/redir.sh

RUN chmod 550 /home/pwn/redir.sh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD ./chall /home/pwn/chall
ADD ./flag.txt /home/pwn/flag.txt
ADD ./pet_sound.txt /home/pwn/pet_sound.txt
RUN chmod 550 /home/pwn/chall

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh

RUN service xinetd restart
