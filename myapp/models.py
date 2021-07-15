from django.db import models
from django import forms
class Document(models.Model):
    filename=models.CharField(max_length=100)
    document = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

class Document_ATS(models.Model):
    filename=models.CharField(max_length=100)
    document = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    # def __unicode__(self):
    #     return self.content

    def __str__(self):
        return self.filename+" "+self.content

   