FROM node:16-buster-slim

COPY app/ /app
WORKDIR /app
RUN npm install

CMD ["node", "./main.js"]