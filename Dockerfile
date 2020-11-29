FROM node:12 as build
WORKDIR /front
COPY package.json /front/package.json
RUN npm install

COPY . /app

RUN npm run build

FROM nginx:1.16
COPY --from=build /front/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


