if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi
echo "Stopping and removing old container..."
sudo docker stop solarrechnerDB
sudo docker rm solarrechnerDB
sudo docker image rm solarrechner_db
echo "Loading image from tar file..."
sudo docker load -i ./TAR/solarrechnerDB.tar
echo "Configuring and starting container..."
sudo docker run -p 3306:3306 --name solarrechnerDB -e MYSQL_ROOT_PASSWORD=iysKhoHdUJzlUlwJertM solarrechner_db
