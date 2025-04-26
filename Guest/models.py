from django.db import models
from Admin.models import *


#Create your models here.
#Userregistration

class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_contact=models.CharField(max_length=50)
    user_gender=models.CharField(max_length=50)
    user_address=models.CharField(max_length=50)
    user_password=models.CharField(max_length=50)
    
    user_photo=models.FileField(upload_to="Assets/File/user")
    user_proof=models.FileField(upload_to="Assets/File/user")
   
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

class tbl_renter(models.Model):
    renter_name=models.CharField(max_length=50)
    renter_email=models.CharField(max_length=50)
    renter_contact=models.CharField(max_length=50)
    renter_address=models.CharField(max_length=50)
    renter_password=models.CharField(max_length=50)
    # renter_type=models.IntegerField(default=0)
    renter_status=models.IntegerField(default=0)
    renter_photo=models.FileField(upload_to="Assets/Files/Renter")
    renter_proof=models.FileField(upload_to="Assets/Files/Renter")

    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

class tbl_repairshop(models.Model):
    repairshop_name=models.CharField(max_length=50)
    repairshop_email=models.CharField(max_length=50)
    repairshop_contact=models.CharField(max_length=50)
    repairshop_address=models.CharField(max_length=50)
    repairshop_password=models.CharField(max_length=50)
    # renter_type=models.IntegerField(default=0)
    repairshop_status=models.IntegerField(default=0)
    repairshop_photo=models.FileField(upload_to="Assets/Files/Repairshop")
    repairshop_proof=models.FileField(upload_to="Assets/Files/Repairshop")

    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
