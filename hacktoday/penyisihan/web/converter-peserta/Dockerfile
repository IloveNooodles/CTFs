FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y nodejs npm ffmpeg && \
    apt-get clean

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir /home/ctf
RUN mkdir /home/ctf/.npm
WORKDIR /home/ctf

COPY package*.json ./

RUN npm install
COPY src/ ./src
COPY flag /{RANDOM-FILE-FLAG}

RUN chown -R root:ctf /{RANDOM-FILE-FLAG}
RUN chown -R www-data:www-data /home/ctf/src/uploads/
RUN chown 999:999 /home/ctf/.npm
RUN chmod 440 /{RANDOM-FILE-FLAG}

USER ctf
EXPOSE 3000

CMD ["npm", "run", "start"]
