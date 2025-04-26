from django.shortcuts import render,redirect,get_object_or_404
from Guest.models import *
from Admin.models import *
from User.models import *
from Renter.models import *
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from .models import tbl_category, tbl_product, tbl_subcategory 
from django.db.models import Avg, Count
from Renter.models import tbl_product  
from User.models import tbl_rating 
 # Ensure these are imported

def Logout(request):
    del request.session['uid']
    return redirect("Guest:Login")

def category_products(request, category_id):
    category = get_object_or_404(tbl_category, id=category_id)
    # Filter products where subcategory belongs to this category
    products = tbl_product.objects.filter(subcategory__category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, "User/CategoryProducts.html", context)


def product_detail(request, product_id):
    # Fetch the product with related reviews using prefetch_related for optimization
    product = get_object_or_404(tbl_product, id=product_id)
    
    # Fetch reviews for this product, optimized with select_related
    reviews = tbl_rating.objects.filter(product=product).select_related('user')
    
    # Calculate average rating and review count
    review_count = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating_data'))['rating_data__avg'] or 0  # Use rating_data instead of rating
    
    # Prepare context for template
    context = {
        'product': product,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
    }
    
    # Debug print to verify data (visible in the server console)
    print(f"Product: {product}")
    print(f"Reviews: {list(reviews)}")  # Convert to list for better visibility
    print(f"Review count: {review_count}")
    print(f"Average rating: {avg_rating}")
    
    return render(request, 'User/ProductDetails.html', context)
    
# Create your views here.
#homepage

def Homepage(request):
    # Only fetch notification counts if user is logged in
    pending_bookings_count = 0
    pending_repairs_count = 0
    product_booking_requests_count = 0
    
    if request.user.is_authenticated:
        # Count pending bookings made by this user
        pending_bookings_count = tbl_booking.objects.filter(
            user=request.user,
            status='Pending'  # Adjust status field name/value as per your model
        ).count()
        
        # Count pending repair requests by this user
        pending_repairs_count = tbl_repair.objects.filter(
            user=request.user,
            status='Pending'  # Adjust status field name/value as per your model
        ).count()
        
        # Count pending booking requests for products added by this user
        product_booking_requests_count = tbl_booking.objects.filter(
            product__user=request.user,  # Assuming product has user field
            status='Pending'  # Adjust status field name/value as per your model
        ).count()
    
    feedback = tbl_feedback.objects.all()
    # Get top-rated products
    top_products = tbl_product.objects.annotate(
        avg_rating=Avg('tbl_rating__rating_data'),  # Average rating per product
        rating_count=Count('tbl_rating')            # Number of ratings
    ).order_by('-avg_rating', '-rating_count')[:4]  # Sort by avg rating, then count, limit to 4
    
    laptops_category = tbl_category.objects.get(category_name="Laptops")
    cameras_category = tbl_category.objects.get(category_name="Camera")
    drones_category = tbl_category.objects.get(category_name="Drone")
    consoles_category = tbl_category.objects.get(category_name="Gaming Consoles")
    
    context = {
        'laptops_category': laptops_category,
        'cameras_category': cameras_category,
        'drones_category': drones_category,
        'consoles_category': consoles_category,
        'feedback': feedback,
        'product': top_products,
        # Add notification counts to context
        'pending_bookings_count': pending_bookings_count,
        'pending_repairs_count': pending_repairs_count,
        'product_booking_requests_count': product_booking_requests_count,
    }
    return render(request, "User/Homepage.html", context)


# Myprofile
def Myprofile(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    return render(request,"User/Myprofile.html",{"user":user})


# Editprofile

def Editprofile(request): 
    user= tbl_user.objects.get(id=request.session['uid']) 
    if request.method=="POST": 
        user.user_name=request.POST.get("txt_name") 
        user.user_email=request.POST.get("txt_email") 
        user.user_address=request.POST.get("txt_address") 
        user.save() 
        return redirect('User:Myprofile') 
    else: 
        return render(request,'User/Editprofile.html',{'user':user})


# Changepassword

def Changepassword(request): 
    user= tbl_user.objects.get(id=request.session['uid']) 
    dbpassword=user.user_password 
    if request.method=="POST": 
        OldPassword=request.POST.get("txt_old") 
        NewPassword=request.POST.get("txt_new") 
        RetypePassword=request.POST.get("txt_retype") 
        if dbpassword==OldPassword: 
            if NewPassword==RetypePassword: 
                user.user_password=NewPassword 
                user.save() 
                return redirect('User:Myprofile') 
            else: 
                return render(request,'User/Changepassword.html',{'msg':"Password mismatach "}) 
        else: 
            return render(request,'User/Changepassword.html',{'msg':'invalid password'}) 
    else: 
        return render(request,'User/Changepassword.html',)


# AddProduct
 
def AddProduct(request):
    pdata=tbl_product.objects.filter(user=request.session['uid'])
    categoryData=tbl_category.objects.all()
    if request.method=='POST':
        tbl_product.objects.create(
        product_name=request.POST.get("txt_name"),
        product_description=request.POST.get("txt_desc"),
        product_price=request.POST.get("txt_price"),       
        subcategory=tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory")),     
        product_photo=request.FILES.get("txt_photo"),
        user=tbl_user.objects.get(id=request.session['uid'])
        )
         
        return render(request,"User/AddProduct.html",{"categoryData":categoryData})
    else:
        return render(request,"User/AddProduct.html",{"categoryData":categoryData,'product':pdata})


def DeleteAddProduct(request,did):
    tbl_product.objects.get(id=did).delete()
    return redirect("User:AddProduct") 

#AddStock

def AddStock(request,did):
    if request.method == "POST":
        tbl_stock.objects.create(stock_quantity=request.POST.get("txt_quantinty"),product=tbl_product.objects.get(id=did))
        return redirect("User:AddStock",did)
    else:
        return render(request,"User/AddStock.html")

#ViewProducts
from django.shortcuts import render
from Renter.models import tbl_product
from User.models import tbl_rating  # Adjust based on your app structure
from django.db.models import Q, Avg

def ViewProducts(request):
    query = request.GET.get('q', '').strip()
    products = tbl_product.objects.all()
    ar=[1,2,3,4,5]
    parry=[]
    avg=0
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(subcategory__category__category_name__icontains=query) |
            Q(subcategory__subcategory_name__icontains=query) |
            Q(product_description__icontains=query)
        )

    for i in products:
        total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_quantity'))['total']
        total_cart = tbl_cart.objects.filter(product=i.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
        # print(total_stock)
        # print(total_cart)
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total =  total_stock - total_cart
        i.total_stock = total

        tot=0
        ratecount=tbl_rating.objects.filter(product=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=i.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
                #print(avg)
            parry.append(avg)
        else:
            parry.append(0)
        # print(parry)
    datas=zip(products,parry)
    return render(request, 'User/ViewProducts.html', {'datas':datas,"ar":ar})


# Gallery

def Gallery(request,id):
    data=tbl_gallery.objects.filter(product=id)
    if request.method == "POST":
        tbl_gallery.objects.create(product_images=request.FILES.get("txt_images"),product=tbl_product.objects.get(id=id))
        return render(request,"User/Gallery.html",{"gallerydata":data}) 
    else:
        return render(request,"User/Gallery.html",{"gallerydata":data})

def DeleteGallery(request,did):
    tbl_gallery.objects.get(id=did).delete()
    return redirect("User:AddProduct") 



def Addcart(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    Userdata=tbl_user.objects.get(id=request.session["uid"])
    bookingcount=tbl_booking.objects.filter(user=Userdata,booking_status=0).count()
    if bookingcount>0:
        bookingdata=tbl_booking.objects.get(user=Userdata,booking_status=0)
        cartcount=tbl_cart.objects.filter(booking=bookingdata,product=productdata).count()
        if cartcount>0:
            msg="Already added"
            return render(request,"User/ViewProducts.html",{'msg':msg})
        else:
            tbl_cart.objects.create(booking=bookingdata,product=productdata)
            msg="Added To cart"
            return render(request,"User/ViewProducts.html",{'msg':msg})
    else:
        bookingdata = tbl_booking.objects.create(user=Userdata)
        tbl_cart.objects.create(booking=tbl_booking.objects.get(id=bookingdata.id),product=productdata)
        msg="Added To cart"
        return render(request,"User/ViewProducts.html",{'msg':msg})

def Mycart(request):
    if "uid" in request.session:
        if request.method=="POST":
            bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
            # bookingdata.booking_amount=request.POST.get("carttotalamt")
            # bookingdata.booking_status=1
            # bookingdata.save()
            # cart = tbl_cart.objects.filter(booking=bookingdata)
            # for i in cart:
            #     i.cart_status = 1
            #     i.save()
            return redirect("User:Bookdetails")
        else:
            bookcount = tbl_booking.objects.filter(user=request.session["uid"],booking_status=0).count()
            if bookcount > 0:
                book = tbl_booking.objects.get(user=request.session["uid"],booking_status=0)
                request.session["bookingid"] = book.id
                cart = tbl_cart.objects.filter(booking=book)
                for i in cart:
                    total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_quantity'))['total']
                    total_cart = tbl_cart.objects.filter(product=i.product.id, cart_status=0).aggregate(total=Sum('cart_qty'))['total']
                    # print(total_stock)
                    # print(total_cart)
                    if total_stock is None:
                        total_stock = 0
                    if total_cart is None:
                        total_cart = 0
                    total =  total_stock - total_cart
                    i.total_stock = total
                return render(request,"User/MyCart.html",{'cartdata':cart})
            else:
                return render(request,"User/MyCart.html")
    else:
        return redirect("Guest:login")
        

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_qty=qty
   cartdata.save()
   return redirect("User:Mycart")   

#Complaint

def Complaint(request,id):
    user= tbl_user.objects.get(id=request.session['uid'])
    cdata=tbl_complaint.objects.filter(user=request.session['uid'])
    data=tbl_complaint.objects.all()
    if request.method=='POST':
        tbl_complaint.objects.create(
            complaint_title=request.POST.get("txt_title"),
            complaint_message=request.POST.get("txt_content"),
            user=user,
            product=tbl_product.objects.get(id=id)),
        return render(request,"User/Complaint.html",{"User":user,"Cdata":cdata})
    else:
        return render(request,"User/Complaint.html",{"User":user,"Cdata":cdata})

def DeleteComplaint(request,did):   
    tbl_complaint.objects.get(id=did).delete()
    return redirect("User:Complaint") 


#Feedback
def Feedback(request):  
    user= tbl_user.objects.get(id=request.session['uid']) 
    # renter= tbl_renter.objects.get(id=request.session['rid'])
    fdata=tbl_feedback.objects.filter(user=request.session['uid'])
    data=tbl_feedback.objects.all()
    if request.method=='POST':
        tbl_feedback.objects.create(
            feedback_title=request.POST.get("txt_feedback"),
            user=user)
        return render(request,"User/Feedback.html",{"User":user,"Fdata":fdata})
    else:
        return render(request,"User/Feedback.html",{"User":user,"Fdata":fdata})

def DeleteFeedback(request,did):
    tbl_feedback.objects.get(id=did).delete()
    return redirect("User:Feedback") 

def MyRentals(request):
    user= tbl_user.objects.get(id=request.session['uid']) 
    renter= tbl_renter.objects.get(id=request.session['rid'])
    fdata=tbl_feedback.objects.filter(user=request.session['uid'])
    data=tbl_feedback.objects.all()
    return redirect("User:MyRentals") 

#Requestrentals

def RequestRepair(request, rid):
    user = tbl_user.objects.get(id=request.session['uid'])
    shop = tbl_repairshop.objects.get(id=rid)
    data = tbl_repair.objects.all()
    if request.method == 'POST':
        tbl_repair.objects.create(
            device_details=request.POST.get("txt_devicedetails"),
            problem_details=request.POST.get("txt_problemdetails"),
            pickup_address=request.POST.get("txt_address"),
            user=user,
            repairshop=shop
        )
        messages.success(request, "Repair request submitted successfully!")
        return redirect("User:MyRepairRequests")
    else:
        return render(request, "User/RequestRepair.html", {"User": user, "data": data})

def ViewRepairshop(request):
    viewrepairshop=tbl_repairshop.objects.all()
    return render(request,"User/ViewRepairShop.html",{'Viewrepairshop':viewrepairshop})


#MyRepairRequests
from django.shortcuts import render
from Repairshop.models import tbl_repair
from .models import tbl_user

def MyRepairRequests(request):
    user = tbl_user.objects.get(id=request.session['uid'])
    rdata = tbl_repair.objects.filter(
        user_id=request.session['uid']
    ).order_by('-request_date')  # Latest first
    return render(request, "User/MyRepairRequests.html", {'repair': rdata})


from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from Repairshop.models import tbl_booking, tbl_cart

def Bookdetails(request):
    try:
        booking = tbl_booking.objects.get(id=request.session['bookingid'])
        
        if request.method == "POST":
            from_date_str = request.POST.get("txt_fromdate")
            to_date_str = request.POST.get("txt_todate")
            
            # Validate date inputs for format only
            try:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
                
                # Update booking
                booking.booking_fordate = from_date_str
                booking.booking_todate = to_date_str
                days_difference = (to_date - from_date).days
                
                cart_items = tbl_cart.objects.filter(booking=booking)
                total_amount = 0
                for item in cart_items:
                    product_price = item.product.product_price
                    total_amount += int(days_difference) * int(product_price)
                    item.cart_status = 1
                    item.save()
                
                booking.booking_amount = total_amount
                booking.booking_status = 1
                booking.save()
                return redirect("User:MyBooking")
            
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, "User/BookDetails.html")
        
        return render(request, "User/BookDetails.html")
    
    except tbl_booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect("User:MyBooking")
    except KeyError:
        messages.error(request, "Please select a booking.")
        return redirect("User:MyBooking")


from datetime import timedelta

def MyBooking(request):
    # Fetch bookings for the user, ordered by booking_date descending
    booking = tbl_booking.objects.filter(
        user=request.session['uid'],
        booking_status__gte=0
    ).order_by('-booking_date')  # Latest first; replace 'booking_date' with your field
    
    # Collect cart items for each booking
    cartdata = []
    for booking_obj in booking:
        carts_for_booking = tbl_cart.objects.filter(booking=booking_obj)
        cartdata.extend(carts_for_booking)
    
    return render(request, "User/MyBooking.html", {'cart': cartdata})


def ProductGallery(request, id):
    product = tbl_product.objects.get(id=id)
    gallery_images = product.gallery_images.all()  
    return render(request, "User/ProductGallery.html", {'product': product, 'gallery_images': gallery_images})

def AjaxSearch(request):
    sub = tbl_product.objects.get(subcategory=request.GET.get("did"))
    place = tbl_place.objects.filter(district=dis)
    return render(request,"Guest/Ajaxsearch.html",{"productdata":sub})

from django.shortcuts import render, get_object_or_404
from .models import tbl_booking, tbl_cart

def Invoice(request, id):
    cart = get_object_or_404(tbl_cart, id=id, booking__user=request.session['uid'])
    booking = cart.booking
    cart_items = tbl_cart.objects.filter(booking=booking)
    
    days = 0
    if booking.booking_fordate and booking.booking_todate:
        days = (booking.booking_todate - booking.booking_fordate).days
    else:
        print(f"Warning: Booking {booking.id} has incomplete dates - From: {booking.booking_fordate}, To: {booking.booking_todate}")
    
    total_amount = 0
    for cart_item in cart_items:
        subtotal = int(cart_item.product.product_price) * int(cart_item.cart_qty) * int(days)
        total_amount += subtotal
    
    context = {
        'booking': booking,
        'cart_items': cart_items,
        'days': days,
        'total_amount': total_amount,
    }
    return render(request, 'User/Invoice.html', context)



def chatpage(request,id):
    renter  = tbl_renter.objects.get(id=id)
    return render(request,"User/Chat.html",{"user":renter})

def ajaxchat(request):
    from_user = tbl_user.objects.get(id=request.session["uid"])
    to_renter = tbl_renter.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),user_from=from_user,renter_to=to_renter,chat_file=request.FILES.get("file"))
    return render(request,"User/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_user.objects.get(id=request.session["uid"])
    chat_data = tbl_chat.objects.filter((Q(user_from=user) | Q(user_to=user)) & (Q(renter_from=tid) | Q(renter_to=tid))).order_by('chat_time')
    return render(request,"User/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(user_from=request.session["uid"]) & Q(renter_to=request.GET.get("tid")) | (Q(renter_from=request.GET.get("tid")) & Q(user_to=request.session["uid"]))).delete()
    return render(request,"User/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})


def ordercancel(request,id):
    cart=tbl_cart.objects.get(id=id)
    cart.cart_status = 5
    cart.save()
    return redirect("User:MyBooking")

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(product=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(product=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user=tbl_user.objects.get(id=request.session['uid'])
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=user,user_review=user_review,rating_data=rating_data,product=tbl_product.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(product=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)


def payment(request,pid):
   booking = tbl_cart.objects.get(id=pid)
   amount = booking.booking.booking_amount
   if request.method == "POST":
      booking.cart_status = 3
      booking.save()
      return redirect("User:loader")
   else:
      return render(request,"User/Payment.html", {"total":amount})

def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def ProductDetails(request):
    return render(request,"User/ProductDetails.html")



def cancel_repair_request(request, repair_id):
    repair = get_object_or_404(tbl_repair, id=repair_id, user__id=request.session['uid'])
    if request.method == "GET":  # Using GET since it’s a link
        # Allow cancellation only if status is Pending, Accepted, or Rejected
        if repair.repair_status in [0, 1, 2]:
            repair.repair_status = 5  # Set to Cancelled
            repair.save()
            messages.success(request, "Repair request cancelled successfully.")
        else:
            messages.error(request, "Cannot cancel this request at this stage.")
    return redirect('User:MyRepairRequests')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from Repairshop.models import tbl_repair
from .models import tbl_user

def RepairPayment(request, repair_id):
    try:
        repair = tbl_repair.objects.get(id=repair_id, user=request.session['uid'])
        if repair.repair_status != 5:
            raise Http404("Payment not allowed for this status.")
        
        amount = repair.repair_amount
        if request.method == "POST":
            payment_method = request.POST.get('payment_method')  # Optional field
            if payment_method == 'cod':  # COD from RepairInvoice
                repair.repair_status = 9  # COD Requested
                repair.save()
                messages.success(request, "COD selected. Payment will be collected on delivery.")
                return redirect("User:MyRepairRequests")
            else:  # Default to online payment if no payment_method or invalid
                repair.repair_status = 6  # Payment Completed
                repair.save()
                messages.success(request, "Payment completed successfully.")
                return redirect("User:loader")
        return render(request, "User/Payment.html", {"total": amount, "repair": repair})
    except tbl_repair.DoesNotExist:
        raise Http404("Repair request not found.")
    except KeyError:
        messages.error(request, "Please log in to make a payment.")

def RepairInvoice(request, repair_id):
    try:
        repair = tbl_repair.objects.get(id=repair_id, user=request.session['uid'])
        if repair.repair_status < 5:
            raise Http404("Invoice not available yet.")
        if not repair.repairshop:
            messages.error(request, "No repair shop assigned to this request.")
            return redirect('User:MyRepairRequests')
        return render(request, 'User/RepairInvoice.html', {'repair': repair})
    except tbl_repair.DoesNotExist:
        raise Http404("Repair request not found.")
    except KeyError:
        messages.error(request, "Please log in to view your invoice.")
        return redirect('User:login')


def ProductBookings(request):
    # Get the logged-in user's ID
    user_id = request.session.get('uid')
    
    # Fetch bookings for products listed by the logged-in user
    bookings = tbl_booking.objects.filter(
        tbl_cart__product__user_id=user_id
    ).distinct()
    
    return render(request, "User/ProductBookings.html", {"bookings": bookings})




def chatpageu(request,id):
    user  = tbl_user.objects.get(id=id)
    return render(request,"User/ChatU.html",{"user":user})

def ajaxchatu(request):
    from_user = tbl_user.objects.get(id=request.session["uid"])
    to_user = tbl_user.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),user_from=from_user,user_to=to_user,chat_file=request.FILES.get("file"))
    return render(request,"User/ChatU.html")

def ajaxchatviewu(request):
    tid = request.GET.get("tid")
    user = tbl_user.objects.get(id=request.session["uid"])
    chat_data = tbl_chat.objects.filter((Q(user_from=user) | Q(user_to=user)) & (Q(user_from=tid) | Q(user_to=tid))).order_by('chat_time')
    return render(request,"User/ChatViewU.html",{"data":chat_data,"tid":int(tid)})

def clearchatu(request):
    tbl_chat.objects.filter(Q(user_from=request.session["uid"]) & Q(user_to=request.GET.get("tid")) | (Q(user_from=request.GET.get("tid")) & Q(user_to=request.session["uid"]))).delete()
    return render(request,"User/ClearChatU.html",{"msg":"Chat Deleted Sucessfully...."})

def ViewBooking(request):
    cart_items = tbl_cart.objects.filter(product__user=request.session['uid'])
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
    
    # Sort by booking_date in descending order
    bookings_with_details = sorted(
        bookings_with_details,
        key=lambda x: x['cart'].booking.booking_date,
        reverse=True
    )
    
    context = {
        'bookings_with_details': bookings_with_details
    }
    return render(request, "User/ViewBooking.html", context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def updatests(request, cart_id, status):
    carcart_item = tbl_cart.objects.get(id=cart_id)
    carcart_item.cart_status = status
    carcart_item.save()
    return redirect('User:ViewBooking')



def chatpager(request,id):
    repairshop  = tbl_repairshop.objects.get(id=id)
    return render(request,"User/Chatr.html",{"user":repairshop})

def ajaxchatr(request):
    from_user = tbl_user.objects.get(id=request.session["uid"])
    to_repairshop = tbl_repairshop.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),user_from=from_user,repairshop_to=to_repairshop,chat_file=request.FILES.get("file"))
    return render(request,"User/Chatr.html")

def ajaxchatviewr(request):
    tid = request.GET.get("tid")
    user = tbl_user.objects.get(id=request.session["uid"])
    chat_data = tbl_chat.objects.filter((Q(user_from=user) | Q(user_to=user)) & (Q(repairshop_from=tid) | Q(repairshop_to=tid))).order_by('chat_time')
    return render(request,"User/ChatViewr.html",{"data":chat_data,"tid":int(tid)})

def clearchatr(request):
    tbl_chat.objects.filter(Q(user_from=request.session["uid"]) & Q(repairshop_to=request.GET.get("tid")) | (Q(repairshop_from=request.GET.get("tid")) & Q(user_to=request.session["uid"]))).delete()
    return render(request,"User/ClearChatr.html",{"msg":"Chat Deleted Sucessfully...."})




# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.http import Http404
# from Repairshop.models import tbl_repair
# from .models import tbl_user

# def process_card_payment(request, repair_id):
#     try:
#         repair = tbl_repair.objects.get(id=repair_id, user__id=request.session['uid'])
#         if repair.repair_status != 5:
#             messages.error(request, "Payment not allowed for this status.")
#             return redirect('User:MyRepairRequests')
        
#         amount = repair.repair_amount
#         # Placeholder for payment gateway integration (e.g., Razorpay)
#         # Example: Create a Razorpay order, redirect to payment page
#         # On success (via callback or webhook):
#         payment_successful = True  # Replace with actual gateway response
        
#         if payment_successful:
#             repair.repair_status = 8  # Payment Completed
#             repair.save()
#             if 'payment_method_' + str(repair_id) in request.session:
#                 del request.session['payment_method_' + str(repair_id)]
#             messages.success(request, "Payment completed successfully.")
#             return redirect('User:MyRepairRequests')
#         else:
#             messages.error(request, "Payment failed. Please try again.")
#             return redirect('User:RepairPayment', repair_id=repair_id)
#     except tbl_repair.DoesNotExist:
#         raise Http404("Repair request not found.")
#     except KeyError:
#         messages.error(request, "Please log in to make a payment.")
#         return redirect('User:login')