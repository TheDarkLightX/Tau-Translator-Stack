FROM node:20-alpine AS build
WORKDIR /app

# copy config & dependency manifests first
COPY package.json tsconfig.json vite.config.ts ./
# tsconfig.json needs to exist; see section 3.2

COPY public ./public
COPY src ./src
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts .
COPY public ./public
COPY src ./src
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
