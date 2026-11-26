from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Users(models.Model):
    name=models.CharField(max_length=100)
    emailid=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=20)
    place=models.CharField(max_length=100)
    pincode=models.IntegerField()
    post=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)

class Expert(models.Model):
    name=models.CharField(max_length=100)
    emailid=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=20)
    place=models.CharField(max_length=100)
    pincode=models.IntegerField()
    post=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    qualification= models.CharField(max_length=100)
    experience= models.CharField(max_length=100)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)

class Video(models.Model):
    title=models.CharField(max_length=100)
    date=models.DateField()
    EXPERT=models.ForeignKey(Expert,on_delete=models.CASCADE)
    video=models.CharField(max_length=100)


class Chat(models.Model):
    USERFROM = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="Fromc")
    USERTO = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="Toc")
    message = models.CharField(max_length=600)
    date= models.DateField()

class Complaints(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=700)
    status=models.CharField(max_length=100)
    reply=models.CharField(max_length=100,default='')
    USER = models.ForeignKey(Users, on_delete=models.CASCADE)

class Review(models.Model):
    CUSTOMER= models.ForeignKey(Users, on_delete=models.CASCADE)
    review= models.CharField(max_length=700)
    date= models.DateField()
    rating= models.FloatField()

class request(models.Model):
    CUSTOMER=models.ForeignKey(Users, on_delete=models.CASCADE)
    date=models.DateField()
    EXPERT=models.ForeignKey(Expert, on_delete=models.CASCADE)
    Status=models.CharField(max_length=100,default="")



class Logs(models.Model):
    CUSTOMER=models.ForeignKey(Users, on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    ipaddress=models.CharField(max_length=100)
    result=models.CharField(max_length=100)