FROM node:20-alpine AS build
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts .
COPY src src
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
