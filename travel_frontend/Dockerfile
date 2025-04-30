# Stage 1: Build
FROM node:22-slim AS builder
WORKDIR /app

# Inject env value explicitly
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY . .

# Use Vite's ability to pick up the env var
RUN npm install && npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
