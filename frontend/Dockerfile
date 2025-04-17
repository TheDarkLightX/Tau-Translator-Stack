# frontend/Dockerfile

# 1) Build stage
FROM node:20-alpine AS build
WORKDIR /app

# Copy Vite & TypeScript config + deps manifest
COPY package.json tsconfig.json vite.config.ts ./

# Copy the HTML entrypoint
COPY index.html ./

# Copy your source
COPY src ./src

# Install and build
RUN npm ci && npm run build

# 2) Production stage: serve with Nginx
FROM nginx:alpine
# Copy the built files
COPY --from=build /app/dist /usr/share/nginx/html
# Copy your custom Nginx config (make sure this exists)
COPY nginx.conf /etc/nginx/conf.d/default.conf

