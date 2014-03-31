#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "You must be a root user" 2>&1
    exit 1
fi

while getopts ":u:p:g:h:P:" opt; do  
    case  $opt in 
        u)      USERNAME=$OPTARG;; 
        p)      PASSWORD=$OPTARG;;
        g)      GROUP=$OPTARG;;
        h)      HOME_FOLDER=$OPTARG;;
        P)      PACKAGES=$OPTARG;;
    esac
done

#echo Username: $USERNAME
#echo Password: $PASSWORD
#echo Group: $GROUP
#echo Home folder: $HOME_FOLDER
#echo Packages: $PACKAGES
#exit 0

PERMISSION_TEST="test_perm.sh"


#Creates a user
groupadd $GROUP
useradd $USERNAME -m -d $HOME_FOLDER -G $GROUP

echo $PASSWORD'\n'$PASSWORD'\n' | sudo passwd $USERNAME

#Remove network access
iptables -A OUTPUT -m owner --uid-owner $USERNAME -j LOG
iptables -A OUTPUT -m owner --uid-owner $USERNAME -j REJECT

#Creates build and run directory
mkdir -p $HOME_FOLDER/build 
mkdir -p $HOME_FOLDER/run

#Installs packages
apt-get update && apt-get install --assume-yes $PACKAGES

#Copies permission test to home dir
cp $PERMISSION_TEST $HOME

chown -R $USERNAME $HOME_FOLDER
