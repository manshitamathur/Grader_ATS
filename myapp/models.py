from django.db import models
from django import forms
class Document(models.Model):
    filename=models.CharField(max_length=150)
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






# class Dicty(models.Model):
#     name      = models.CharField(max_length=50)
#     def __str__(self):
#         return self.name

# class KeyVal(models.Model):
#     container = models.ForeignKey(Dicty, db_index=True,on_delete=models.CASCADE)
#     key       = models.CharField(max_length=240, db_index=True)
#     value     = models.TextField(null=True)
class Domains(models.Model):
    name=models.CharField(max_length=150)
    Skills_list = models.TextField()
    Projects_List = models.TextField()
    def __str__(self):
         return self.name


   