from django.shortcuts import render,redirect
from Guest.models import *
from Renter.models import *
from Admin.models import *
from User.models import *
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Renter.models import tbl_product, tbl_category, tbl_subcategory, tbl_renter


def Logout(request):
    del request.session['rid']
    return redirect("Guest:Login")

#Homepage
def RenterHomePage(request):
    if "rid" not in request.session:
        return redirect("Guest:index")
    return render(request,"Renter/RenterHomePage.html")


# Myprofile
def MyProfile(request):
    if "rid" not in request.session:
        return redirect("Guest:index")
    renter=tbl_renter.objects.get(id=request.session['rid'])
    return render(request,"Renter/MyProfile.html",{"renter":renter})


# Editprofile

def EditProfile(request): 
    if "rid" not in request.session:
        return redirect("Guest:index")
    renter= tbl_renter.objects.get(id=request.session['rid']) 
    if request.method=="POST": 
        renter.renter_name=request.POST.get("txt_name") 
        renter.renter_email=request.POST.get("txt_email") 
        renter.renter_address=request.POST.get("txt_address") 
        renter.save() 
        return redirect('Renter:MyProfile') 
    else: 
        return render(request,'Renter/EditProfile.html',{'renter':renter})


# Changepassword

def ChangePassword(request): 
    renter= tbl_renter.objects.get(id=request.session['rid']) 
    dbpassword=renter.renter_password 
    if request.method=="POST": 
        OldPassword=request.POST.get("txt_old") 
        NewPassword=request.POST.get("txt_new") 
        RetypePassword=request.POST.get("txt_retype") 
        if dbpassword==OldPassword: 
            if NewPassword==RetypePassword: 
                renter.user_password=NewPassword 
                renter.save() 
                return redirect('Renter:MyProfile') 
            else: 
                return render(request,'Renter/ChangePassword.html',{'msg':"Password mismatach "}) 
        else: 
            return render(request,'Renter/ChangePassword.html',{'msg':'invalid password'}) 
    else: 
        return render(request,'Renter/ChangePassword.html',)


# AddProduct
 


def DeleteAddProduct(request, did):
    
    product = get_object_or_404(tbl_product, id=did, renter__id=request.session['rid'])
    if request.method == 'POST':
        
        product.delete()
        return redirect('Renter:AddProduct')  
    else:
        
        return render(request, 'Renter/ConfirmDelete.html', {'product': product})

def AddProduct(request):
    if "rid" not in request.session:
        return redirect("Guest:index")

    pdata = tbl_product.objects.filter(renter=request.session['rid'])
    categoryData = tbl_category.objects.all()
    if request.method == 'POST':
        tbl_product.objects.create(
            product_name=request.POST.get("txt_name"),
            product_description=request.POST.get("txt_desc"),
            product_price=request.POST.get("txt_price"),
            subcategory=tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory")),
            product_photo=request.FILES.get("txt_photo"),
            renter=tbl_renter.objects.get(id=request.session['rid'])
        )
        return render(request, "Renter/AddProduct.html", {'categoryData': categoryData, 'product': pdata})
    else:
        return render(request, "Renter/AddProduct.html", {'product': pdata, 'categoryData': categoryData})

#Ajax-Addproduct
def AjaxSubcategory(request):
    dis = tbl_category.objects.get(id=request.GET.get("did"))
    subcategory = tbl_subcategory.objects.filter(category=dis)
    return render(request,"Renter/AjaxSubcategory.html",{"subcategorydata":subcategory})

#AddStock

def AddStock(request,id):
    if request.method == "POST":
        tbl_stock.objects.create(stock_quantity=request.POST.get("txt_quantinty"),product=tbl_product.objects.get(id=id))
        return redirect("Renter:AddStock",id)
    else:
        return render(request,"Renter/AddStock.html")



#Gallery

def Gallery(request,id):
    data=tbl_gallery.objects.filter(product=id)
    if request.method == "POST":
        tbl_gallery.objects.create(product_images=request.FILES.get("txt_images"),product=tbl_product.objects.get(id=id))
        return render(request,"Renter/Gallery.html",{"gallerydata":data}) 
    else:
        return render(request,"Renter/Gallery.html",{"gallerydata":data})

def DeleteGallery(request,did):
    tbl_gallery.objects.get(id=did).delete()
    return redirect("Renter:AddProduct") 

#ViewComplaints

def ViewComplaints(request):
    if "rid" not in request.session:
        return redirect("Guest:index")
    complaint=tbl_complaint.objects.filter(renter=request.session['rid'])
    return render(request,"Renter/ViewComplaints.html",{"Complaint":complaint})
    
def ViewBooking(request):
    if "rid" not in request.session:
        return redirect("Guest:index")
    cart_items = tbl_cart.objects.filter(product__renter=request.session['rid'])
    bookings_with_details = []
    
    for cart in cart_items:
        booking = cart.booking
        days = 0
        if booking.booking_fordate and booking.booking_todate:
            days = (booking.booking_todate - booking.booking_fordate).days
        amount = int(cart.product.product_price) * int(cart.cart_qty) * int(days) if days > 0 else 0
        
        bookings_with_details.append({
            'cart': cart,
            'days': days,
            'amount': amount
        })
    
    
    bookings_with_details = sorted(
        bookings_with_details,
        key=lambda x: x['cart'].booking.booking_date,
        reverse=True
    )
    
    context = {
        'bookings_with_details': bookings_with_details
    }
    return render(request, "Renter/ViewBooking.html", context)


def chatpage(request,id):
    user  = tbl_user.objects.get(id=id)
    return render(request,"Renter/Chat.html",{"user":user})

def ajaxchat(request):
    from_renter = tbl_renter.objects.get(id=request.session["rid"])
    to_user = tbl_user.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),renter_from=from_renter,user_to=to_user,chat_file=request.FILES.get("file"))
    return render(request,"Renter/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_renter.objects.get(id=request.session["rid"])
    chat_data = tbl_chat.objects.filter((Q(renter_from=user) | Q(renter_to=user)) & (Q(user_from=tid) | Q(user_to=tid))).order_by('chat_time')
    return render(request,"Renter/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(renter_from=request.session["rid"]) & Q(user_to=request.GET.get("tid")) | (Q(user_from=request.GET.get("tid")) & Q(renter_to=request.session["uid"]))).delete()
    return render(request,"Renter/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})


def updatests(request,id,sts):
    cart=tbl_cart.objects.get(id=id)
    cart.cart_status = sts
    cart.save()
    return redirect("Renter:ViewBooking")


from django.db.models import Sum, Q, ExpressionWrapper, FloatField, Value
from django.db.models.functions import Cast
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

def SalesProfits(request):
    if "rid" not in request.session:
        return redirect("Guest:index")
    try:
        renter = tbl_renter.objects.get(id=request.session['rid'])
        orders = tbl_cart.objects.filter(
            product__renter=renter,
            cart_status__in=[1, 2, 3, 4, 5]
        ).select_related('booking', 'product').order_by('-booking__booking_fordate')
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                orders = orders.filter(
                    booking__booking_fordate__range=[start_date, end_date]
                )
                print(f"Filtered orders between {start_date} and {end_date}: {orders.count()}")
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        elif start_date or end_date:
            messages.warning(request, "Please provide both start and end dates.")

        # Calculate metrics with Cast
        completed_orders = orders.filter(cart_status__gte=3)
        total_sales = completed_orders.annotate(
            amount_as_float=Cast('booking__booking_amount', FloatField())
        ).aggregate(total=Sum('amount_as_float'))['total'] or 0
        
        profit_expression = ExpressionWrapper(
            Cast('booking__booking_amount', FloatField()) * 0.90,
            output_field=FloatField()
        )
        profit_data = completed_orders.aggregate(total_profit=Sum(profit_expression))
        total_profit = profit_data['total_profit'] or 0
        
        pending_payment_count = orders.filter(cart_status=2).count()
        pending_payment_amount = orders.filter(cart_status__lte=1).annotate(
            amount_as_float=Cast('booking__booking_amount', FloatField())
        ).aggregate(total=Sum('amount_as_float'))['total'] or 0
        order_count = completed_orders.count()

        # Precompute profit per order
        orders_with_profit = []
        for order in orders:
            try:
                booking_amount = float(order.booking.booking_amount) if order.booking.booking_amount else 0
                profit = booking_amount * 0.90  # Profit after 10% commission
            except (ValueError, TypeError) as e:
                print(f"Error calculating profit for order {order.id}: {order.booking.booking_amount}, Error: {e}")
                profit = 0
            orders_with_profit.append({
                'order': order,
                'profit': profit
            })

        context = {
            'renter': renter,
            'total_sales': total_sales,
            'pending_payments': pending_payment_count,
            'pending_payment_amount': pending_payment_amount,
            'total_profit': total_profit,
            'order_count': order_count,
            'orders_with_profit': orders_with_profit  # Updated key
        }
        
        return render(request, "Renter/SalesProfits.html", context)
    except tbl_renter.DoesNotExist:
        messages.error(request, "Renter not found. Please log in.")
        return redirect('Renter:login')
    except KeyError:
        messages.error(request, "Please log in to view sales and profit.")
        return redirect('Renter:login')