FROM nginx:1.23.1-alpine

ADD ../public/templates /usr/share/nginx/html/

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]