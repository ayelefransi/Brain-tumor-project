# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

# Replace hardcoded localhost backend with relative /api for production
COPY . .
RUN grep -R -l "http://localhost:9000" src || true
RUN find src -type f -exec sed -i 's|http://localhost:9000|/api|g' {} +

RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]