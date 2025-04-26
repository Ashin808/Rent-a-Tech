from django.db import models
from Admin.models import *
from Guest.models import *
# Create your models here.
class tbl_product(models.Model):
    product_name=models.CharField(max_length=50)
    product_description=models.CharField(max_length=50)
    product_price=models.CharField(max_length=50)
    product_photo=models.FileField(upload_to="Assets/File/renter")
    subcategory=models.ForeignKey(tbl_subcategory,on_delete=models.CASCADE)
    renter=models.ForeignKey(tbl_renter,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)

class tbl_stock(models.Model):
    stock_quantity=models.CharField(max_length=50)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)

class tbl_gallery(models.Model):
    product_images=models.FileField(upload_to="Assets/File/renter")
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE, related_name="gallery_images")
