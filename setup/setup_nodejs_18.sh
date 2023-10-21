#!/usr/bin/bash
sudo apt update && sudo apt install curl -y
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.profile
nvm install 18
npm install -g npm@latest
npm install -g @vue/cli
node --version
npm --version
vue --version
