FROM node:latest

RUN mkdir -p /ctf
WORKDIR /ctf
COPY . .

RUN chmod 444 flag.txt

# Install library that required by puppeter
RUN apt-get update -y && \
    apt install -y libx11-xcb1 \
    libxcomposite1 libxcursor1 \
    libxdamage1 libxi-dev libxtst-dev \
    libnss3 libcups2 libxss1 libxrandr2 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libpangocairo-1.0-0 libgtk-3-0 libgbm1 -y
RUN yarn install

EXPOSE 1337
ENV PORT=1337
ENV URL=http://ctf.tcp1p.com:25982

CMD yarn start