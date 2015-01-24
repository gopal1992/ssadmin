set -v
git pull
git checkout production
kill -HUP `ps aux | grep emperor | grep -v grep | awk '{print $2}'`
sudo service nginx restart
