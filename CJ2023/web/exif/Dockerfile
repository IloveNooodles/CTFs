FROM node
RUN mkdir -p /app
WORKDIR /app
COPY --chown=www-data:www-data src .
RUN npm install
USER nobody
CMD node /app/index.js