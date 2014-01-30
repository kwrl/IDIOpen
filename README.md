Gentlecoding
---------------

Programming for IDIOpen

* documents: https://drive.google.com/#folders/0B0kLIN3j9tQ5c21NbFc1eHoybGM
* openshift-admin: https://openshift.redhat.com/app/console/applications
* website: it2901-gentlecoding.rhcloud.com
* jenkins: jenkins-gentlecoding.rhcloud.com
* openshift-github: ssh://52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com/~/git/it2901.git/
* openshift SSH: ssh 52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com
* sounddrop spotify: http://open.soundrop.fm/s/XN9jBJxMqazaBOZL

dev contact:

* andsild@gmail.com, andesil@stud.ntnu.no, 91 80 20 57
* filip.egge@gmail.com, filipfe@stud.ntnu.no, 94809127
* kitteeeeeeh@gmail.com, aakongk@stud.ntnu.no, 
* haakon.konrad@gmail.com, 98044242
* Fosse, 91369708
* tinolazreg@gmail.com, 90173005

To get github up and running for production, replace your .git/config file
with the "config" provided in this directory.

The **openshift remote** is LIVE, and pushes will be put on the webserver.
"git push openshift" achieves this.
The **master** branch is supposed to stay clean, but it is only on github (not live)

When pushing to production, you should push to *both* branches.
Do this by typing **git push all**


Django project directory structure
----------------------------------

     djangoproj/
        .gitignore
     	.openshift/
     		README.md
     		action_hooks/  (Scripts for deploy the application)
     			build
     			post_deploy
     			pre_build
     			deploy
     			secure_db.py
     		cron/
     		markers/
     	setup.py   (Setup file with de dependencies and required libs)
     	README.md
     	libs/   (Adicional libraries)
     	data/	(For not-externally exposed wsgi code)
     	wsgi/	(Externally exposed wsgi goes)
     		application (Script to execute the application on wsgi)
     		openshift/	(Django project directory)
     			__init__.py
     			manage.py
     			openshiftlibs.py
     			settings.py
     			urls.py
     			views.py
     			wsgi.py
     			templates/
     				home/
     					home.html (Default home page, change it)
     		static/	(Public static content gets served here)
     			README

From HERE you can start with your own application.
