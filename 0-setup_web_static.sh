#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

server_loc="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
file_path="/etc/nginx/sites-available/default"
sudo apt-get update --yes
sudo apt-get install nginx --yes
sudo mkdir --parents "/data/web_static/releases/test/"
sudo mkdir "/data/web_static/shared/"
echo "Holberton" > "/data/web_static/releases/test/index.html"
rm --force "/data/web_static/current"; ln --symbolic "/data/web_static/releases/test/" "/data/web_static/current"
sudo chown --no-dereference --recursive ubuntu:ubuntu "/data/"
sudo sed -i "29i\ $server_loc" "$file_path"
sudo service nginx restart
