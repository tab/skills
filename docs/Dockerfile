FROM node:24-alpine@sha256:e67514e5d0f6c46656005e1b693b2ec9d52e80b641307de684d4a015ba7a4eaf AS build

WORKDIR /app
ENV ASTRO_TELEMETRY_DISABLED=1

COPY docs/package.json docs/package-lock.json ./docs/
RUN cd docs && npm ci

COPY docs/ ./docs/
COPY plugins/tab/assets/toolbox.svg ./plugins/tab/assets/toolbox.svg

RUN cd docs && npm run build

FROM nginx:1.29-alpine@sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de

COPY docs/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/docs/dist /usr/share/nginx/html/skills

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
