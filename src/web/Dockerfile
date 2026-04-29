# ── Stage 1: Build Angular ───────────────────────────────────────────────────
FROM mcr.microsoft.com/mirror/docker/library/node:20 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN node node_modules/@angular/cli/bin/ng.js build --configuration production

# ── Stage 2: Serve with nginx ────────────────────────────────────────────────
FROM mcr.microsoft.com/mirror/docker/library/nginx:1.25

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy nginx config as a template (envsubst will substitute ${API_UPSTREAM} at runtime)
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy built Angular app
COPY --from=builder /app/dist/delinquency-website /usr/share/nginx/html

EXPOSE 80

# nginx official image auto-runs envsubst on /etc/nginx/templates/*.template
CMD ["nginx", "-g", "daemon off;"]
