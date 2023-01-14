FROM denoland/deno:latest

RUN mkdir -p /ctf
WORKDIR /ctf
COPY ./src/ .
COPY ./makefile .

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

ENV FLAG="Bukan Flag Asli"
RUN deno cache main.ts

USER ctf

ENV PORT=1337
EXPOSE 1337
CMD deno run --no-prompt \
    --allow-env \
    --allow-read \
    --allow-net \
    main.ts