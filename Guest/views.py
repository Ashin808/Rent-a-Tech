from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
# Create your views here.

from django.shortcuts import render
from Renter.models import tbl_product
from User.models import tbl_feedback, tbl_rating  # Adjust if feedback/rating are elsewhere
from django.db.models import Avg, Count

def index(request):
    # Fetch feedbacks
    feedback = tbl_feedback.objects.all()

    # Get top-rated products
    top_products = tbl_product.objects.annotate(
        avg_rating=Avg('tbl_rating__rating_data'),  # Average rating per product
        rating_count=Count('tbl_rating')            # Number of ratings
    ).order_by('-avg_rating', '-rating_count')[:4]  # Sort by avg rating, then count, limit to 4

    context = {
        'product': top_products,  # Matches template's 'product' variable
        'feedback': feedback,
    }
    return render(request, "Guest/index.html", context)

#Ajax
def ajaxplace(request):
    dis = tbl_district.objects.get(id=request.GET.get("did"))
    place = tbl_place.objects.filter(district=dis)
    return render(request,"Guest/AjaxPlace.html",{"placedata":place})

#UserRegistration
def UserRegistration(request):
    data=tbl_user.objects.all()
    data=tbl_place.objects.all()
    districtData=tbl_district.objects.all()
    if request.method=='POST':
        tbl_user.objects.create(
        user_name=request.POST.get("txt_name"),
        user_email=request.POST.get("txt_email"),
        user_password=request.POST.get("txt_password"),
        # user_confirmpassword=request.POST.get("txt_confirmpassword"),
        place=tbl_place.objects.get(id=request.POST.get("sel_place")),
        user_gender = request.POST.get("gender"),
        user_contact=request.POST.get("txt_contact"),
        user_address=request.POST.get("txt_address"),
        user_photo=request.FILES.get("txt_photo"),
        user_proof=request.FILES.get("txt_proof"),
        )
        
        return render(request,"Guest/UserRegistration.html",{"districtData":districtData,"User":data})
    else:
        return render(request,"Guest/UserRegistration.html",{"districtData":districtData,"User":data})


#Renter Registration

def RenterRegistration(request):
    data=tbl_renter.objects.all()
    data=tbl_place.objects.all()
    districtData=tbl_district.objects.all()
    if request.method=='POST':
        tbl_renter.objects.create(
        renter_name=request.POST.get("txt_name"),
        renter_email=request.POST.get("txt_email"),
        renter_password=request.POST.get("txt_password"),
        # user_confirmpassword=request.POST.get("txt_confirmpassword"),
        place=tbl_place.objects.get(id=request.POST.get("sel_place")),
        renter_contact=request.POST.get("txt_contact"),
        renter_address=request.POST.get("txt_address"),
        renter_photo=request.FILES.get("txt_photo"),
        renter_proof=request.FILES.get("txt_proof"),
        )
        
        return render(request,"Guest/RenterRegistration.html",{"districtData":districtData,"User":data})
    else:
        return render(request,"Guest/RenterRegistration.html",{"districtData":districtData,"User":data})


# RepairshopRegistration
def RepairshopRegistration(request):
    data=tbl_repairshop.objects.all()
    data=tbl_place.objects.all()
    districtData=tbl_district.objects.all()
    if request.method=='POST':
        tbl_repairshop.objects.create(
        repairshop_name=request.POST.get("txt_name"),
        repairshop_email=request.POST.get("txt_email"),
        repairshop_password=request.POST.get("txt_password"),
        # user_confirmpassword=request.POST.get("txt_confirmpassword"),
        place=tbl_place.objects.get(id=request.POST.get("sel_place")),
        repairshop_contact=request.POST.get("txt_contact"),
        repairshop_address=request.POST.get("txt_address"),
        repairshop_photo=request.FILES.get("txt_photo"),
        repairshop_proof=request.FILES.get("txt_proof"),
        )
        
        return render(request,"Guest/RepairshopRegistration.html",{"districtData":districtData,"User":data})
    else:
        return render(request,"Guest/RepairshopRegistration.html",{"districtData":districtData,"User":data})

# Login

def Login(request):
    if request.method == "POST":
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        
        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        rentercount=tbl_renter.objects.filter(renter_email=email,renter_password=password).count()
        repairshop=tbl_repairshop.objects.filter(repairshop_email=email,repairshop_password=password).count()
        admincount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        if usercount > 0:
            user=tbl_user.objects.get(user_email=email,user_password=password)
            request.session["uid"]=user.id
            return redirect("User:Homepage")

        elif rentercount > 0:
            renter=tbl_renter.objects.get(renter_email=email,renter_password=password)
            if renter.renter_status == 1:
                request.session["rid"]=renter.id
                return redirect("Renter:RenterHomePage")
            elif renter.renter_status == 2:
                return render(request,"Guest/Login.html",{'msg':"Login Rejected"})
                

        elif admincount > 0:
            admin=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session["aid"]=admin.id
            return redirect("Admin:AdminHomepage")

        elif repairshop > 0:
            repairshop=tbl_repairshop.objects.get(repairshop_email=email,repairshop_password=password)
            if repairshop.repairshop_status == 1:
                request.session["sid"]=repairshop.id
                return redirect("Repairshop:RepairshopHomepage")
            elif repairshop.repairshop_status == 2:
                return render(request,"Guest/Login.html",{'msg':"Login Rejected"})
            
        else:
            return render(request,"Guest/Login.html",{'msg':"Invalid Email Or Password"})
    else:
        return render(request,"Guest/Login.html")