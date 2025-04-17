# Build stage using Node.js
FROM node:20-alpine AS build
WORKDIR /app

# Copy package.json, tsconfig.json, and vite.config.ts first
COPY package.json tsconfig.json vite.config.ts ./

# Copy the rest of the app files
COPY public ./public
COPY src ./src

# Install dependencies and build the app
RUN npm ci && npm run build

# Nginx stage to serve the app
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

