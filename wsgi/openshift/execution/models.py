from django.db import models

class FileExtension(models.Model):
    extension = models.CharField(max_length=4)

class CompilerProfile(models.Model):
    extensions = models.ManyToManyField(FileExtension)
    compiler_name_cmd = models.CharField(max_length=10)

    flags = models.CharField(max_lenght=100)
    # How do we handle output filename

    package_name = models.CharField(max_length=30)

# EOF
