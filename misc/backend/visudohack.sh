#!/bin/sh
if [ -z "$1" ]; then
  echo "Starting up visudo with this script as first parameter"
  export EDITOR=$0 && sudo -E visudo
else
  echo "Changing sudoers"
  echo "www-data ALL = NOPASSWD: /bin/su $SANDBOX_USER [^&|]*" >> $1
fi
