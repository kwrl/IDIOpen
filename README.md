Gentlecoding
---------------

Programming for IDIOpen

* _documents_: https://drive.google.com/#folders/0B0kLIN3j9tQ5c21NbFc1eHoybGM
* _openshift-admin_: https://openshift.redhat.com/app/console/applications
* _website_: it2901-gentlecoding.rhcloud.com
* _jenkins_: jenkins-gentlecoding.rhcloud.com
* _openshift-github_: ssh://52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com/~/git/it2901.git/
* _openshift SSH_: ssh 52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com

* _sounddrop spotify_: http://open.soundrop.fm/s/XN9jBJxMqazaBOZL

dev contact:

* andsild@gmail.com, andesil@stud.ntnu.no, 91 80 20 57
* filip.egge@gmail.com, filipfe@stud.ntnu.no, 94809127
* kitteeeeeeh@gmail.com, aakongk@stud.ntnu.no, 
* haakon.konrad@gmail.com, 98044242
* Fosse, 91369708
* tinolazreg@gmail.com, 90173005

To get github up and running for production, replace your .git/config file
with the "config" provided in this directory.

The *openshift* branch is LIVE, and will be put on the webserver.
You can push this by writing "git push openshift".
The *master* branch is supposed to stay clean, but it is only on github (not live)

To push to *BOTH*, which is what you want ideally, write "git push all"
the command *git push* (without any branch specified) should default to push 
to master


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
