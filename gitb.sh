#!/bin/bash
read -p 'ip address: ' IP_ADDR
BASE_URL="http://$IP_ADDR:8080"
URL="$BASE_URL/api/v3/"
while :
do
	read -p 'Drag and drop your directory: ' DIR_PATH
  echo
  RAND=$(echo $RANDOM | tr '[0-9]' '[a-z]')
	echo "$(basename $DIR_PATH)-$RAND"
	REPO="$(basename $DIR_PATH)-$RAND"
	curl -u root:root -X POST -H "Accept: application/vnd.github.v3+json" ${URL}user/repos -d "{\"name\":\"$REPO\"}"
  cd $DIR_PATH || exit
	git init
	git add .
	git commit -m "Initial Commit"
	git remote add origin "$BASE_URL/git/root/$REPO.git"
	git push -u origin master
#	rm -rf .git
done



