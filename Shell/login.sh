#!/bin/bash
clear
read -p "Enter host username: " username
read -p "Enter passwd: " passwd
printf "\n"

curl -L -s -b keks.jar -c keks.jar https://isis.tu-berlin.de/auth/shibboleth/index.php -o silence
#steal the cookie

curl -L -s -b keks.jar -c keks.jar -d "j_username=$username&j_password=$passwd&Submit=Login" https://shibboleth.tubit.tu-berlin.de/idp/Authn/UserPassword -o silence
#gives login data with stolen cookie to make shibboleth happy

curl -L -b keks.jar https://isis.tu-berlin.de/my/
#to enter isis directly with cookie.

rm silence
#because it's just data





#we have now turned shit into gold.
