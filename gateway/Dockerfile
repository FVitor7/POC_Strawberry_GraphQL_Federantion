FROM node:14

WORKDIR /app

COPY package* /app/

RUN npm ci

COPY . /app/

EXPOSE 7000

#CMD npm run dev