
Django on OpenShift
===================

This git repository helps you get up and running quickly w/ a Django
installation on OpenShift.  The Django project name used in this repo
is 'openshift' but you can feel free to change it.  Right now the
backend is sqlite3 and the database runtime is @
$OPENSHIFT_DATA_DIR/sqlite3.db.

Before you push this app for the first time, you will need to change
the Django admin password (see below). Then, when you first push this
application to the cloud instance, the sqlite database is copied from
wsgi/openshift/sqlite3.db with your newly changed login
credentials. Other than the password change, this is the stock
database that is created when 'python manage.py syncdb' is run with
only the admin app installed.

On subsequent pushes, a 'python manage.py syncdb' is executed to make
sure that any models you added are created in the DB.  If you do
anything that requires an alter table, you could add the alter
statements in GIT_ROOT/.openshift/action_hooks/alter.sql and then use
GIT_ROOT/.openshift/action_hooks/deploy to execute that script (make
sure to back up your database w/ 'rhc app snapshot save' first :) )


Running on OpenShift
--------------------

Create an account at http://openshift.redhat.com/

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc

Create a python-2.6 application

    rhc app create -a django -t python-2.6

Add this upstream repo

    cd django
    git remote add upstream -m master git://github.com/openshift/django-example.git
    git pull -s recursive -X theirs upstream master

Set your Django admin password. (Django must be installed on your dev system for this to work; 'sudo yum install Django' will do this for Fedora and RHEL)

    cd wsgi/openshift
    ./manage.py changepassword admin
    
Then push the repo upstream

    cd ../../
    git push

That's it, you can now checkout your application at (default admin account is admin/admin):

    http://django-$yournamespace.rhcloud.com
