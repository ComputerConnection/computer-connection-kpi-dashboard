FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY src ./src
COPY public ./public
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
