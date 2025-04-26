from django.db import models
from Admin.models import *
from Guest.models import *
from Renter.models import *
# Create your models here.

# Complaint
class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=50)
    complaint_message=models.CharField(max_length=50)
    complaint_reply=models.CharField(max_length=50)
    complaint_status = models.IntegerField(default=0)
    complaint_date = models.DateField(auto_now_add=True) 
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True)
    renter=models.ForeignKey(tbl_renter,on_delete=models.CASCADE,null=True)


class tbl_booking(models.Model):
    booking_date = models.DateField(auto_now_add=True)
    booking_amount = models.CharField(max_length=30)
    booking_status = models.IntegerField(default=0)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    booking_fordate=models.DateField(null=True)
    booking_todate=models.DateField(null=True)
    

class tbl_cart(models.Model):
    cart_qty = models.IntegerField(default=1)
    cart_status = models.IntegerField(default=0)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    booking = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)

class tbl_feedback(models.Model):
    feedback_title=models.CharField(max_length=50)
    feedback_date = models.DateField(auto_now_add=True) 
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    renter=models.ForeignKey(tbl_renter,on_delete=models.CASCADE,null=True)
    
class tbl_repair(models.Model):
    request_date = models.DateField(auto_now_add=True)
    repair_status = models.IntegerField(default=0)
    device_details=models.CharField(max_length=50)
    problem_details=models.CharField(max_length=50)
    date_scheduled=models.DateField(null=True)
    pickup_address=models.CharField(max_length=50)
    repair_notes=models.CharField(max_length=50)
    repair_amount=models.CharField(max_length=50)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    repairshop=models.ForeignKey(tbl_repairshop,on_delete=models.CASCADE,null=True)
      
class tbl_chat(models.Model):
    chat_content = models.CharField(max_length=500)
    chat_time = models.DateTimeField()
    chat_file = models.FileField(upload_to='ChatFiles/')
    user_from = models.ForeignKey(tbl_user,on_delete=models.CASCADE,related_name="user_from",null=True)
    user_to = models.ForeignKey(tbl_user,on_delete=models.CASCADE,related_name="user_to",null=True)
    renter_from = models.ForeignKey(tbl_renter,on_delete=models.CASCADE,related_name="renter_from",null=True)
    renter_to = models.ForeignKey(tbl_renter,on_delete=models.CASCADE,related_name="renter_to",null=True)
    repairshop_from = models.ForeignKey(tbl_repairshop,on_delete=models.CASCADE,related_name="repairshop_from",null=True)
    repairshop_to = models.ForeignKey(tbl_repairshop,on_delete=models.CASCADE,related_name="repairshop_to",null=True)


class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    user_review=models.CharField(max_length=500)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)