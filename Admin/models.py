from django.db import models


# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)

class tbl_brand(models.Model):
    brand_name=models.CharField(max_length=50)

class tbl_type(models.Model):
    type_name=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_subtype(models.Model):
    subtype_name=models.CharField(max_length=50)
    Type=models.ForeignKey(tbl_type,on_delete=models.CASCADE)
# Department
class tbl_department(models.Model):
    department_name=models.CharField(max_length=50)
# Designation
class tbl_designation(models.Model):
    designation_name=models.CharField(max_length=50)
# Staff
class tbl_staff(models.Model):
    staff_name=models.CharField(max_length=50)
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
    designation=models.ForeignKey(tbl_designation,on_delete=models.CASCADE)
    staff_contact=models.CharField(max_length=50)
    staff_basicsallary=models.CharField(max_length=50)