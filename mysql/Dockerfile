FROM mysql:5.7
COPY init_db.sql /docker-entrypoint-initdb.d/
ENV MYSQL_DATABASE=data_db \
    MYSQL_ROOT_PASSWORD=password
EXPOSE 3306
