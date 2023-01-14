FROM denoland/deno:latest

RUN mkdir -p /ctf
WORKDIR /ctf
COPY . .

RUN apt-get -y update
RUN apt-get -y install chromium

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PORT=1337 \
    DOMAIN="ctf.tcp1p.com"

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
RUN chown -R ctf:ctf /ctf

RUN chmod 444 flag.txt

RUN deno cache main.ts
RUN deno run -A --unstable https://deno.land/x/puppeteer@16.2.0/install.ts

USER ctf
EXPOSE 1337
CMD deno run --allow-all main.ts