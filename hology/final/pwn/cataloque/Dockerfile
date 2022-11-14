FROM ubuntu

RUN apt-get update \
    && apt-get install -y xinetd gnupg

RUN touch /var/log/xinetdlog

ENV USER cataloque

WORKDIR /home/$USER

RUN useradd $USER

COPY challenge/wrapper.sh /home/$USER/
COPY challenge/$USER /home/$USER/
COPY challenge/elysia /home/$USER/elysia

COPY ./flag.txt /flag.txt
RUN chmod 444 /flag.txt

COPY ./config/$USER.xinetd /etc/xinetd.d/$USER

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER

EXPOSE 1337

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog