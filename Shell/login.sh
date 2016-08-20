#!/bin/bash
clear

#bold text
bold=$(tput bold)
normal=$(tput sgr0)

#get column rows to display title of the programm in the middle [fancy.sh]
COLUMNS=$(tput cols) 
title="~Shell Login Script~" 
printf "%*s\n" $(((${#title}+$COLUMNS)/2)) "$title"
#[/fancy.sh]

read -p "Enter hostname: " username
read -s -p "Enter passwd: " passwd
# -s command silences the input of the passwd (you can also display asterisk but need improvement)
echo
printf 'login you in...'
#log in
redirectedURL=$(curl $1 -s -L -I -b Cookies/keks.jar -c Cookies/keks.jar -o /dev/null -w '%{url_effective}' https://isis.tu-berlin.de/auth/shibboleth/index.php)
echo -ne '...'
secondRedirectURL=$(curl $1 -s -L -b Cookies/keks.jar -c Cookies/keks.jar -w '%{url_effective}' -d "'shib_idp_ls_exception.shib_idp_session_ss=&shib_idp_ls_success.shib_idp_session_ss=false&shib_idp_ls_value.shib_idp_session_ss=&shib_idp_ls_exception.shib_idp_persistent_ss=&shib_idp_ls_success.shib_idp_persistent_ss=false&shib_idp_ls_value.shib_idp_persistent_ss=&shib_idp_ls_supported=&_eventId_proceed='" -o /dev/null $redirectedURL )
echo -ne '...'
curl -s -L -b Cookies/keks.jar -c Cookies/keks.jar --data 'j_username=$username&j_password=$passwd&_eventId_proceed=' $secondRedirectURL -o Homepage/InformationSystemforStudents.html
echo -ne '...'
echo
benutzerName=$(grep -o 'Profil anzeigen">.*</a>' homepage.html | cut -f2- -d'>' | cut -f1 -d'<' )
echo Sie sind angemeldet als ${bold}${benutzerName}${normal}
echo Ihre ISIS seite befindet sich im Ordner ${bold}Homepage/${normal}
echo viel Spaß!
echo
