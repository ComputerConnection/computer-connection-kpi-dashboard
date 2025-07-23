FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* tsconfig.json vite.config.ts ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
