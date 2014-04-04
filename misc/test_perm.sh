#/bin/bash


# TODO: try touch ${PWD} instead to avoid ever creating the file, more clean?
#if [ -n $(touch testfile) ]; then
#	echo "Write permission, lol"
#fi

#if [ -n $(ping -c 5 www.googlek.com) ]; then
#	echo "Network access, lol"
#fi

READ_FILE="/dev/zero"
WRITE_FILE="/dev/null"
PING_COUNT=5
PING_HOST="www.google.com"

function test_read
{
	if [ -r $READ_FILE ]; then
		error "Read permission."
		return 2
	fi

	passed "No read permission."	
	return 0
}

function test_write
{
	if [ -w $WRITE_FILE ]; then
		error "Write permission."
		return 2
	fi

	passed "No write permission"
	return 0
}

function test_network
{
	for interface in $(ls /sys/class/net/ | grep -v lo);
	do
  		if [[ $(cat /sys/class/net/$interface/carrier) = 1 ]]; then OnLine=1; fi
	done
	if ! [ $OnLine ]; then 
		passed "No network access."  
		return 0
	else
		error "Network access."	
		return 2
	fi
}

function error
{
	echo "[ERROR] " $1 >&2
}

function passed
{
	echo "[PASSED] " $1
}


RETURN_CODE=0

test_read
ret=$?
RETURN_CODE=$(($RETURN_CODE + $ret))

test_write
ret=$?
RETURN_CODE=$(($RETURN_CODE + $ret))

test_network
ret=$?
RETURN_CODE=$(($RETURN_CODE + $ret))

exit $RETURN_CODE
# EOF 
