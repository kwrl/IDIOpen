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

echo Username: $USERNAME
echo Password: $PASSWORD
echo Group: $GROUP
echo Home folder: $HOME_FOLDER
echo Packages: $PACKAGES

PERMISSION_TEST="test_perm.sh"

print_usage() {
    echo "Parameters needed:"
    echo "-g [GROUPNAME]"
    echo "-u [USERNAME]"
    echo "-p [PASSWORD]"
    echo "-h [HOME_DIR]"
    echo "-P [PACKAGES NEEDED]"
}

if [ -z $GROUP ] || [ -z $USERNAME ] || [ -z $PASSWORD ] || [ -z $HOME_FOLDER ] || [ -z $PACKAGES ]
then
    print_usage
    exit 1
fi


#Creates a user
function create_user
{
	echo -n "Creating user group" $GROUP ".. "
	groupadd $GROUP 
	echo -n "Creating user " $USERNAME ".. "
	useradd $USERNAME -m -d $HOME_FOLDER -G $GROUP
	echo -n "Setting password.."
	echo $PASSWORD'\n'$PASSWORD'\n' | sudo passwd $USERNAME
}

function remove_network_access
{
	echo -n "Setting up network attempt log.. "
	iptables -A OUTPUT -m owner --uid-owner $USERNAME -j LOG

	echo -n "Reject network access.. "
	iptables -A OUTPUT -m owner --uid-owner $USERNAME -j REJECT
}

#Creates build and run directory
function create_directories
{
	mkdir -p $HOME_FOLDER/build 
	mkdir -p $HOME_FOLDER/run
}

#Installs packages
function install_packages
{
	apt-get update && apt-get install --assume-yes $PACKAGES
}

chown -R $USERNAME $HOME_FOLDER













