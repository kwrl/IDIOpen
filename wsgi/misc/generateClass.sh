apps="article contest userregistration"

for apps in ${apps}; do echo $apps; python ./manage.py graph_models -g -e -l dot -o ${apps}.png ${apps}; done
