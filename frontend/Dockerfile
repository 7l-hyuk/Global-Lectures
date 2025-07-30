# Step 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY ./frontend .
RUN npm install && npm run build

# Step 2: Serve with nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY ./frontend/nginx.conf /etc/nginx/nginx.conf
