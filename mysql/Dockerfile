# FROM mysql:5.7
# COPY init_db.sql /docker-entrypoint-initdb.d/
# ENV MYSQL_DATABASE=data_db \
#    MYSQL_ROOT_PASSWORD=password
FROM mysql:latest
COPY ./my.cnf /etc/mysql/my.cnf
COPY ./init_db.sql /docker-entrypoint-initdb.d/init_db.sql
#CMD ["mysqld", "-c", "/etc/mysql/my.cnf"]
EXPOSE 3306

