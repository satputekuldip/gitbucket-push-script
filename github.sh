#!/bin/bash
URL="https://api.github.com/"
while :
do
	read -p 'Drag and drop your directory: ' DIR_PATH
  echo
  RAND=$(echo $RANDOM | tr '[0-9]' '[a-z]')
	echo "$(basename $DIR_PATH)-$RAND"
	REPO="$(basename $DIR_PATH)-$RAND"
	curl -u {username}:{token} -X POST -H "Accept: application/vnd.github.v3+json" -H "Authorization: token {token}" ${URL}user/repos -d "{\"name\":\"$REPO\",\"private\":true}"
         cd $DIR_PATH || exit
	git init
	git add .
	git commit -m "Initial Commit"
	git branch -M master
	git remote add origin "git@github.com:{username}/$REPO.git"
	git push -u origin master
done
