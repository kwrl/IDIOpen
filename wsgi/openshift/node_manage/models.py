from django.db import models

class ExecutionNode(models.Model):
    name = models.CharField(max_length=20)
    dest_ip = models.IPAddressField()
    password = models.CharField(max_length=50)

# EOF
