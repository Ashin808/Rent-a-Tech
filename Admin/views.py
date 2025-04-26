from django.shortcuts import render,redirect, get_object_or_404
from Admin.models import *
from Guest.models import *
from Renter.models import *
from User.models import *
from django.contrib.auth.decorators import login_required
from User.models import tbl_booking, tbl_cart  
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from User.models import tbl_cart
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta # Adjust app if needed
from User.models import tbl_repair  

def Logout(request):
    del request.session['aid']
    return redirect("Guest:Login")



def booking_detail(request, booking_id):
    booking = get_object_or_404(tbl_booking, id=booking_id)
    cart_items = tbl_cart.objects.filter(booking=booking).select_related('product__renter')
    
    days = 0
    if booking.booking_fordate and booking.booking_todate:
        days = (booking.booking_todate - booking.booking_fordate).days
    
    grand_total = 0
    for cart in cart_items:
        # Convert product_price to float or decimal if it’s a string
        price = float(cart.product.product_price) if isinstance(cart.product.product_price, str) else cart.product.product_price
        qty = int(cart.cart_qty) if isinstance(cart.cart_qty, str) else cart.cart_qty
        subtotal = price * qty * days
        grand_total += subtotal
    
    context = {
        'booking': booking,
        'cart_items': cart_items,
        'days': days,
        'grand_total': grand_total,
    }
    return render(request, 'Admin/BookingDetails.html', context)



def District(request):
    data=tbl_district.objects.all()
    if request.method=='POST':
        tbl_district.objects.create(district_name=request.POST.get("txt_district"))
        return render(request,"Admin/District.html",{"District":data})
    else:
        return render(request,"Admin/District.html",{"District":data})


def DeleteDistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect("Admin:District")

def EditDistrict(request,eid):
    dis=tbl_district.objects.get(id=eid)
    if request.method == "POST":
        dis.district_name=request.POST.get("txt_district")
        dis.save()
        return redirect("Admin:District")
    else:
        return render(request,'Admin/District.html',{'edit':dis})






def Category(request):
    data=tbl_category.objects.all()
    if request.method=='POST':
        tbl_category.objects.create(category_name=request.POST.get("txt_category"))
        return render(request,"Admin/Category.html",{"Category":data})
    else:
        return render(request,"Admin/Category.html",{"Category":data})

def DeleteCategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect("Admin:Category")

def EditCategory(request,eid):
    dis=tbl_category.objects.get(id=eid)
    if request.method == "POST":
        dis.category_name=request.POST.get("txt_category")
        dis.save()
        return redirect("Admin:Category")
    else:
        return render(request,'Admin/Category.html',{'edit':dis})







def Admin(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    data=tbl_admin.objects.all()
    if request.method=='POST':
        tbl_admin.objects.create(admin_name=request.POST.get("txt_name"),admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password"))
        return render(request,"Admin/Admin.html",{"Admin":data})
    else:
        return render(request,"Admin/Admin.html",{"Admin":data})

def DeleteAdmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect("Admin:Admin")


def Brand(request):
    data=tbl_brand.objects.all()
    if request.method=='POST':
        tbl_brand.objects.create(brand_name=request.POST.get("txt_brand"))
        return render(request,"Admin/brand.html",{"Brand":data})
    else:
        return render(request,"Admin/brand.html",{"Brand":data})

def DeleteBrand(request,did):
    tbl_brand.objects.get(id=did).delete()
    return redirect("Admin:Brand") 

def Type(request):
    data=tbl_type.objects.all()
    if request.method=='POST':
        tbl_type.objects.create(type_name=request.POST.get("txt_type"))
        return render(request,"Admin/type.html",{"Type":data})
    else:
        return render(request,"Admin/type.html",{"Type":data})


def DeleteType(request,did):
    tbl_type.objects.get(id=did).delete()
    return redirect("Admin:Type") 


# place
def Place(request):
    data=tbl_place.objects.all()
    districtData=tbl_district.objects.all()
    if request.method=='POST':
        dis = tbl_district.objects.get(id=request.POST.get('sel_district'))

        tbl_place.objects.create(place_name=request.POST.get("txt_place"),district=dis)
        return render(request,"Admin/Place.html",{"districtData":districtData,"seldata":data})
    else:
        return render(request,"Admin/Place.html",{"districtData":districtData,"seldata":data})

def DeletePlace(request,did):
    tbl_place.objects.get(id=did).delete()
    return redirect("Admin:Place")

def EditPlace(request,eid):
    districtData=tbl_district.objects.all()
    dis=tbl_place.objects.get(id=eid)
    if request.method == "POST":
        dis.place_name=request.POST.get("txt_place")
        dis.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        dis.save()
        return redirect("Admin:Place")
    else:
        return render(request,'Admin/Place.html',{"districtData":districtData,'edit':dis})


# Subcategory

def Subcategory(request):
    data=tbl_subcategory.objects.all()
    categoryData=tbl_category.objects.all()
    if request.method=='POST':
        dis = tbl_category.objects.get(id=request.POST.get('sel_category'))

        tbl_subcategory.objects.create(subcategory_name=request.POST.get("txt_sub"),category=dis)
        return render(request,"Admin/Subcategory.html",{"categoryData":categoryData,"seldata":data})
    else:
        return render(request,"Admin/Subcategory.html",{"categoryData":categoryData,"seldata":data})

def DeleteSubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return redirect("Admin:Subcategory")

def EditSubcategory(request,eid):
    categoryData=tbl_category.objects.all()
    dis=tbl_subcategory.objects.get(id=eid)
    if request.method == "POST":
        dis.subcategory_name=request.POST.get("txt_sub")
        dis.category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        dis.save()
        return redirect("Admin:Subcategory")
    else:
        return render(request,'Admin/subcategory.html',{'edit':dis})

# subtype
def Subtype(request)  :
    data=tbl_subtype.objects.all()
    typeData=tbl_type.objects.all()
    if request.method=="POST":
        dis = tbl_type.objects.get(id=request.POST.get('sel_type'))
        tbl_subtype.objects.create(subtype_name=request.POST.get("txt_sub"),Type=dis)
        return render(request,"Admin/Subtype.html",{"typeData":typeData})
    else:
        return render(request,"Admin/Subtype.html",{"typeData":typeData})

# Department
def Department(request):
    data=tbl_department.objects.all()
    if request.method=='POST':
        tbl_department.objects.create(department_name=request.POST.get("txt_department"))
        return render(request,"Admin/Department.html",{"Department":data})
    else:
        return render(request,"Admin/Department.html",{"Department":data})

def DeleteDepartment(request,did):
    tbl_department.objects.get(id=did).delete()
    return redirect("Admin:Department")

def EditDepartment(request,eid):
    departmentData=tbl_department.objects.all()
    dis=tbl_department.objects.get(id=eid)
    if request.method == "POST":
        dis.department_name=request.POST.get("txt_department")
        dis.save()
        return redirect("Admin:Department")
    else:
        return render(request,'Admin/Department.html',{'edit':dis})

# Designation
def Designation(request):
    data=tbl_designation.objects.all()
    if request.method=='POST':
        tbl_designation.objects.create(designation_name=request.POST.get("txt_designation"))
        return render(request,"Admin/Designation.html",{"Designation":data})
    else:
        return render(request,"Admin/Designation.html",{"Designation":data})


def DeleteDesignation(request,did):
    tbl_designation.objects.get(id=did).delete()
    return redirect("Admin:Designation")

def EditDesignation(request,eid):
    designationData=tbl_designation.objects.all()
    dis=tbl_designation.objects.get(id=eid)
    if request.method == "POST":
        dis.designation_name=request.POST.get("txt_designation")
        dis.save()
        return redirect("Admin:Designation")
    else:
        return render(request,'Admin/Designation.html',{'edit':dis})

# Staff

def Staff(request):
    data=tbl_staff.objects.all()
    departmentData=tbl_department.objects.all()
    designationData=tbl_designation.objects.all()
    if request.method=='POST':
        dis = tbl_department.objects.get(id=request.POST.get('sel_department'))
        des = tbl_designation.objects.get(id=request.POST.get('sel_designation'))
        tbl_staff.objects.create(staff_name=request.POST.get("txt_name"),staff_contact=request.POST.get("txt_contact"),staff_basicsallary=request.POST.get("txt_bsallary"),department=dis,designation=des)
        return render(request,"Admin/Staff.html",{"departmentData":departmentData,"designationData":designationData,"seldata":data})
    else:
        return render(request,"Admin/Staff.html",{"departmentData":departmentData,"designationData":designationData,"seldata":data})


def DeleteStaff(request,did):
    tbl_staff.objects.get(id=did).delete()
    return redirect("Admin:Staff")

def EditStaff(request,eid):
    staffData=tbl_staff.objects.all()
    departmentData=tbl_department.objects.all()
    designationData=tbl_designation.objects.all()
    dis=tbl_staff.objects.get(id=eid)
    if request.method == "POST":
        dis.staff_name=request.POST.get("txt_name")
        dis.staff_contact=request.POST.get("txt_contact")
        dis.staff_basicsallary=request.POST.get("txt_bsallary")
        dis.department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        dis.designation=tbl_designation.objects.get(id=request.POST.get("sel_designation"))
        dis.save()
        return redirect("Admin:Staff")
    else:
        return render(request,'Admin/Staff.html',{"departmentData":departmentData,"designationData":designationData,'edit':dis})


# Renter Approval

def RenterApproval(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    renter=tbl_renter.objects.all()
    return render(request,"Admin/RenterApproval.html",{'renter':renter})

def acceptr(request,acid):
    acc=tbl_renter.objects.get(id=acid)
    acc.renter_status=1
    acc.save()
    return redirect('Admin:RenterApproval')

def rejectr(request,reid):
    acc=tbl_renter.objects.get(id=reid)
    acc.renter_status=2
    acc.save()
    return redirect('Admin:RenterApproval')


#ViewUsers
def ViewUsers(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    user=tbl_user.objects.all()
    return render(request,"Admin/ViewUsers.html",{'User':user})


#ViewRenters
def ViewRenters(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    renter=tbl_renter.objects.filter(renter_status=1)
    return render(request,"Admin/ViewRenters.html",{'Renter':renter})

#ViewRepairshop
def ViewRepairshop(request): 
    if "aid" not in request.session:
        return redirect("Guest:index")
    repairshop = tbl_repairshop.objects.filter(repairshop_status=1)  # Assuming 'renter_status' is the correct field
    return render(request, "Admin/ViewRepairshop.html", {'Repairshop': repairshop})  # Changed 'Renter' to 'renters' for consistency



#ViewProducts
def ViewProducts(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    products=tbl_product.objects.all()
    return render(request,"Admin/ViewProducts.html",{'Products':products})

#ViewComplaints
def ViewComplaints(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    complaint=tbl_complaint.objects.filter(complaint_status=0)
    replied=tbl_complaint.objects.filter(complaint_status=1)
    return render(request,"Admin/ViewComplaints.html",{"Complaint":complaint,"Replied":replied})

# ViewFeedback
def ViewFeedbacks(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    feedback=tbl_feedback.objects.all()
    return render(request,"Admin/ViewFeedbacks.html",{"Feedback":feedback})

#AddReply
def AddReply(request,id):
    complaint = tbl_complaint.objects.get(id=id)
    if request.method == "POST": 
        complaint.complaint_reply=request.POST.get("txt_reply")
        complaint.complaint_status=1  # Assuming 1 means replied
        complaint.save()
        return redirect("Admin:ViewComplaints")
    else:
        return render(request,"Admin/AddReply.html",)

#RepairshopApproval
def RepairshopApproval(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    repairshop=tbl_repairshop.objects.all()
    return render(request,"Admin/RepairshopApproval.html",{'repair':repairshop})

def accept(request,acid):
    acc=tbl_repairshop.objects.get(id=acid)
    acc.repairshop_status=1
    acc.save()
    return redirect('Admin:RepairshopApproval')

def reject(request,reid):
    acc=tbl_repairshop.objects.get(id=reid)
    acc.repairshop_status=2
    acc.save()
    return redirect('Admin:RepairshopApproval')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from User.models import tbl_cart
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from User.models import tbl_cart 
from User.models import tbl_repair 


def AdminHomepage(request):
    if "aid" not in request.session:
        return redirect("Guest:index")
    # Original renter code (unchanged)
    cart_items = tbl_cart.objects.select_related('booking__user', 'product__renter').order_by('-booking__booking_date')[:10]
    # Filter out cancelled transactions (adjust 'cart_status' to your field name)
    recent_transactions = tbl_cart.objects.select_related('booking__user').filter(
        cart_status__iexact='4'  # Assuming 'completed' means not cancelled
    ).order_by('-booking__booking_date')[:4]
    
    for transaction in recent_transactions:
        total_amount = float(transaction.booking.booking_amount)
        transaction.admin_commission = total_amount * 0.10
        
        # Convert booking_date (DateField) to datetime for subtraction
        booking_datetime = datetime.combine(transaction.booking.booking_date, datetime.min.time())
        time_diff = timezone.now() - timezone.make_aware(booking_datetime)
        minutes_ago = int(time_diff.total_seconds() / 60)
        transaction.time_ago = f"{minutes_ago} minutes ago" if minutes_ago < 60 else f"{minutes_ago // 60} hours ago"

    # New repair shop transaction code using tbl_repair
    recent_shoptransactions = tbl_repair.objects.select_related('user').filter(
        repair_status__iexact='8'  # Assuming '8' is completed; adjust based on your data
    ).order_by('-request_date')[:4]  # Match renter limit

    for transaction in recent_shoptransactions:
        total_amount = float(transaction.repair_amount)
        transaction.admin_commission = total_amount * 0.10 if not hasattr(transaction, 'admin_commission') else float(transaction.admin_commission)

    context = {
        'cart': cart_items,
        'recent_transactions': recent_transactions,  # Keep original renter transactions
        'recent_shoptransactions': recent_shoptransactions,  # Add repair shop transactions
    }
    return render(request, 'Admin/AdminHomepage.html', context)


# Admin/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from User.models import tbl_cart
from django.utils import timezone
from datetime import datetime, timedelta


def all_transactions(request):
    # Filter out cancelled transactions
    transactions = tbl_cart.objects.select_related('booking__user').filter(
        cart_status__iexact='4'  # Adjust 'cart_status' and 'completed' to your field/value
    ).order_by('-booking__booking_date')
    
    # Calculate total admin profit (excluding cancelled)
    total_profit = 0
    daily_profits = {}
    daily_amounts = {}
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    for t in transactions:
        try:
            amount = float(t.booking.booking_amount)
            profit = amount * 0.10
            total_profit += profit
            date_key = t.booking.booking_date
            if start_date.date() <= date_key <= end_date.date():
                daily_profits[date_key] = daily_profits.get(date_key, 0) + profit
                daily_amounts[date_key] = daily_amounts.get(date_key, 0) + amount
        except (ValueError, TypeError):
            continue  # Skip invalid amounts

    # Prepare chart data
    labels = [d.strftime('%Y-%m-%d') for d in sorted(daily_profits.keys())] or [timezone.now().strftime('%Y-%m-%d')]
    profit_data = [daily_profits[d] for d in sorted(daily_profits.keys())] or [0]
    amount_data = [daily_amounts[d] for d in sorted(daily_amounts.keys())] or [0]

    context = {
        'transactions': transactions,
        'total_profit': total_profit,
        'chart_labels': labels,
        'chart_data': profit_data,
        'chart_amounts': amount_data,
    }
    return render(request, 'Admin/AllTransactions.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from User.models import tbl_repair


def repair_transactions(request):
    # Filter out cancelled transactions (adjust 'repair_status' value based on your model)
    transactions = tbl_repair.objects.select_related('user').filter(
        repair_status__iexact='8'  # Assuming '4' is completed; adjust as needed
    ).order_by('-request_date')

    # Calculate total admin profit (excluding cancelled)
    total_profit = 0
    daily_profits = {}
    daily_amounts = {}
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    for t in transactions:
        try:
            amount = float(t.repair_amount)  # Direct access to repair_amount
            profit = amount * 0.10
            total_profit += profit
            date_key = t.request_date if t.request_date else timezone.now()
            if start_date <= date_key <= end_date:
                daily_profits[date_key] = daily_profits.get(date_key, 0) + profit
                daily_amounts[date_key] = daily_amounts.get(date_key, 0) + amount
        except (ValueError, TypeError):
            continue  # Skip invalid amounts

    # Prepare chart data (match renter's format)
    labels = [d.strftime('%Y-%m-%d') for d in sorted(daily_profits.keys())] or [timezone.now().strftime('%Y-%m-%d')]
    chart_data = [daily_profits[d] for d in sorted(daily_profits.keys())] or [0]
    chart_amounts = [daily_amounts[d] for d in sorted(daily_amounts.keys())] or [0]

    # Recent transactions (last 7 days)
    recent_repair_transactions = tbl_repair.objects.select_related('user').filter(
        request_date__gte=timezone.now() - timedelta(days=7),
        repair_status__iexact='4'
    ).order_by('-request_date')[:5]

    context = {
        'recent_repair_transactions': recent_repair_transactions,
        'transactions': transactions,  # Match renter's context key
        'total_profit': total_profit,  # Match renter's context key
        'chart_labels': labels,        # Match renter's context key
        'chart_data': chart_data,      # Match renter's context key
        'chart_amounts': chart_amounts # Match renter's context key
    }
    return render(request, 'Admin/RepairTransactions.html', context)