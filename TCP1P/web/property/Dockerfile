FROM denoland/deno:latest

RUN mkdir -p /ctf
WORKDIR /ctf

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
RUN chown -R ctf:ctf /ctf

COPY . .

RUN chmod 444 flag.txt
RUN deno cache main.ts

USER ctf
ENV PORT=1337 \
    DB_FILE_NAME="session.db" \
    SESSION_COOKIE_NAME="property_chall_session"

CMD deno run --allow-all main.ts