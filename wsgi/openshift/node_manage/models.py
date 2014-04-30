from django.db import models

class ExecutionNode(models.Model):
	'''
	This model is not yet in use. Though intended to represent the execution
	nodes used to evaluate tasks. 
	'''
    name = models.CharField(max_length=20)
    dest_ip = models.IPAddressField()
    password = models.CharField(max_length=50)

# EOF
