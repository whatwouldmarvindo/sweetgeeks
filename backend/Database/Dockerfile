# Derived from official mysql image (our base image)
FROM mysql
# Add a database
ENV MYSQL_DATABASE solarrechnerDB
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./SQL/ /docker-entrypoint-initdb.d/
