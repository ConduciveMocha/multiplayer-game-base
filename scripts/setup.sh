sudo apt-get update


sudo apt-get upgrade python3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


sudo apt-get install mysql-server 


sudo apt-get install redis-server
sudo systemctl enable redis-server.service


curl -sS https://dl.yarnpkg.com//debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
yarn install


cd logs
touch engineio.log
touch serverlog.log
touch socketio.log
touch testlog.log
cd ..
