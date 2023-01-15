FROM node:alpine

RUN mkdir -p /ctf
WORKDIR /ctf
COPY . .

RUN chmod 444 flag.txt

RUN adduser -D ctf
RUN echo "ctf:ctf" | chpasswd
RUN yarn install

USER ctf
EXPOSE 8080
CMD node index.js