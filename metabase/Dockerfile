FROM metabase/metabase:latest
#COPY metabase.settings /settings.yml
#CMD ["metabase", "--config", "/settings.yml"]

# METABASE_DB_TYPE: "mysql"
# METABASE_DB_HOST: "mysql" # Replace with your MySQL container name (e.g., "mysql")
# METABASE_DB_PORT: 3306
# METABASE_DB_USER: "dba" # Replace with your MySQL username
# METABASE_DB_PASS: "A1YTsqilzHkUQ4" # Replace with your MySQL password

ENV MB_DB_CONNECTION_URI: jdbc:mysql://mysql:3306/metabase?user=dba&password=A1YTsqilzHkUQ4&allowPublicKeyRetrieval=true&useSSL=false