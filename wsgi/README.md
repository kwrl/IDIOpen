Gentlecoding
---------------

Programming for IDIOpen

* documents: https://drive.google.com/#folders/0B0kLIN3j9tQ5c21NbFc1eHoybGM
* openshift-admin: https://openshift.redhat.com/app/console/applications
* website: http://it2901-gentlecoding.rhcloud.com
* jenkins: http://jenkins-gentlecoding.rhcloud.com
* openshift-github: ssh://52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com/~/git/it2901.git/
* openshift SSH: ssh 52e4349a5004466b76000045@it2901-gentlecoding.rhcloud.com
* sounddrop spotify: http://open.soundrop.fm/s/XN9jBJxMqazaBOZL

dev contact:
-----------------

* andsild@gmail.com, andesil@stud.ntnu.no, 91 80 20 57
* filip.egge@gmail.com, filipfe@stud.ntnu.no, 94809127
* kitteeeeeeh@gmail.com, aakongk@stud.ntnu.no, 
* haakon.konrad@gmail.com, 98044242
* Fosse, 91369708
* tinolazreg@gmail.com, 90173005

Git configuration
--------------------------

Replace your .git/config file
with the "config" provided in this directory.

**"cp -vi <gitfolder>/config/gitconfig <gitfolder>/.git/config"**

The **openshift remote** is LIVE, and pushes will be put on the webserver.
"git push openshift" achieves this.
The **master** branch is supposed to stay clean, but it is only on github (not live)

When pushing to production, you should push to *both* remotes/branches.
Do this by typing **git push all**


Django project directory structure
----------------------------------

     djangoproj/
        .gitignore
     	.openshift/
     		action_hooks/         ( Scripts invoked when pushing to openshift)
     			build
     			post_deploy
     			pre_build
     			deploy
     			secure_db.py
     		cron/
     		markers/
     	setup.py                  ( Setup file that should install/verify dependencies in building)
     	libs/                     ( Adicional libraries)
     	data/                     ( For not-externally exposed wsgi code)
     	wsgi/                     ( Externally exposed wsgi goes)
     		application           ( Script to execute the application on wsgi)
     		openshift/            ( Django project directory)
     			templates/
     				home/
     					home.html ( Default home page)
     		static/               ( Public static content gets served here)
