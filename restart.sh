set -v

git pull
kill -HUP `ps aux | grep emperor | grep -v grep | awk '{print $2}'`
sudo service nginx restart

