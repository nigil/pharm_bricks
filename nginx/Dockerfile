FROM nginx:1.13

EXPOSE 80 443

RUN mkdir -p /etc/nginx/sites-enabled

COPY ./pb.crt /etc/ssl/certs/
COPY ./pb.key /etc/ssl/private/
COPY ./nginx.conf /etc/nginx/
COPY ./pb.conf /etc/nginx/sites-enabled/
COPY ./run.sh ./

CMD bash -c ./run.sh