FROM node:18-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --quiet
COPY . .
EXPOSE 8080
CMD ["npx", "ts-node", "server.ts"]
