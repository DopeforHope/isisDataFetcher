#!/bin/bash
clear

#get column rows to display title of the programm in the middle [fancy.sh]
COLUMNS=$(tput cols) 
title="+++++~Shell Login Script~+++++" 
printf "%*s\n" $(((${#title}+$COLUMNS)/2)) "$title"
#[/fancy.sh]

# check if the dire

if [ ! -d "cookieJar" ]; then
  echo a first time for everything!
fi

if [ -d "cookieJar" ]; then
  # Shit there is no goto statement in bash, i'll probably separate this in another bash script and load the separeted scripts indidually
 #should go in here: curl -L -b cookieJar/isis.jar https://isis.tu-berlin.de/my/ --progress-bar -o homepage.html

 echo you have done this before, havent you?
fi

read -p "Enter hostname: " username
read -s -p "Enter passwd: " passwd
# -s command silences the input of the passwd (you can also display asterisk but need improvement)
echo
echo loggin you in...

#log in
#need a variable setting for cookieJar/isis.jar (too long, to type)
curl -L -s -b cookieJar/isis.jar -c cookieJar/isis.jar https://isis.tu-berlin.de/auth/shibboleth/index.php -o silence
#steal the cookie

curl -L -s -b cookieJar/isis.jar -c cookieJar/isis.jar -d "j_username=$username&j_password=$passwd&Submit=Login" https://shibboleth.tubit.tu-berlin.de/idp/Authn/UserPassword -o silence
#gives login data with stolen cookie to make shibboleth happy

curl -L -b cookieJar/isis.jar https://isis.tu-berlin.de/my/ -o homepage.html
#to enter isis directly with cookie.

rm silence
#because it's just data
echo game over





#we have now turned shit into gold.
