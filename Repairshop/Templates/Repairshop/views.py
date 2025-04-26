# from django.shortcuts import render, redirect, get_object_or_404
# from Guest.models import *
# from Admin.models import *
# from Renter.models import *
# from User.models import *
# from Repairshop.models import *
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.http import Http404
# from .models import tbl_repair, tbl_repairshop
# from django.shortcuts import render
# from django.contrib import messages
# from Repairshop.models import tbl_repair, tbl_repairshop
# from django.db.models import Sum




# def Logout(request):
#     del request.session['sid']
#     return redirect("Guest:Login")


# def RepairshopHomepage(request):
#     return render(request, "Repairshop/RepairshopHomepage.html")

# def ViewRepairRequest(request):
#     repairshop = tbl_repairshop.objects.get(id=request.session['sid'])  # Use sid for repairshop
#     data = tbl_repair.objects.filter(
#         repairshop=repairshop
#     ).order_by('-request_date')  # Latest first
#     return render(request, "Repairshop/ViewRepairRequest.html", {"repair_requests": data})

    
# def update_request(request, request_id):
#     repair = get_object_or_404(tbl_repair, id=request_id, repairshop__id=request.session['sid'])
#     if request.method == "POST":
#         new_status = request.POST.get('repair_status')
#         if new_status is not None:
#             repair.repair_status = int(new_status)
#             repair.save()
#             if new_status == "1":
#                 messages.success(request, "Request accepted.")
#             elif new_status == "2":
#                 messages.success(request, "Request rejected.")
#             elif new_status == "3":
#                 messages.success(request, "Request marked as in progress.")
#             elif new_status == "4":
#                 messages.success(request, "Request marked as completed.")
#             elif new_status == "6":
#                 messages.success(request, "Payment Succesful.")
#         repair_amount = request.POST.get('repair_amount')
#         if repair_amount:
#             repair.repair_amount = float(repair_amount)
#             repair.save()
#             messages.success(request, "Amount updated successfully.")
#         return redirect('Repairshop:ViewRepairRequest')
#     return redirect('Repairshop:ViewRepairRequest')

# def revert_cancellation(request, request_id):
#     repair = get_object_or_404(tbl_repair, id=request_id, repairshop__id=request.session['sid'])
#     if request.method == "GET" and repair.repair_status == 5:
#         repair.repair_status = 0  # Revert to Pending
#         repair.save()
#         messages.success(request, "Cancellation reverted. Request is now pending.")
#     return redirect('Repairshop:ViewRepairRequest')

# def edit_request(request, request_id):
#     repair = get_object_or_404(tbl_repair, id=request_id, repairshop__id=request.session['sid'])
#     if request.method == "POST":
#         repair.date_scheduled = request.POST.get("txt_date")
#         repair.repair_notes = request.POST.get("txt_notes")
#         repair.save()
#         messages.success(request, "Request details updated.")
#         return redirect('Repairshop:ViewRepairRequest')
#     return render(request, 'Repairshop/EditRequest.html', {'repair': repair})

# def reject(request, reid):
#     repair = get_object_or_404(tbl_repair, id=reid, repairshop__id=request.session['sid'])
#     if repair.repair_status == 0:  # Only reject if pending
#         repair.repair_status = 2
#         repair.save()
#         messages.success(request, "Request rejected.")
#     return redirect('Repairshop:ViewRepairRequest')

# def RequestForm(request, id):
#     repair = get_object_or_404(tbl_repair, id=id, repairshop__id=request.session['sid'])
#     if request.method == "POST":
#         repair.date_scheduled = request.POST.get("txt_date")
#         repair.repair_notes = request.POST.get("txt_notes")
#         repair.repair_status = 1
#         repair.save()
#         return redirect('Repairshop:ViewRepairRequest')
#     return render(request, 'Repairshop/RequestForm.html')

# # MyProfile
# def MyProfile(request):
#     repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#     return render(request, "Repairshop/MyProfile.html", {"repairshop": repairshop})

# # EditProfile
# def EditProfile(request):
#     repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#     if request.method == "POST":
#         repairshop.repairshop_name = request.POST.get("txt_name")
#         repairshop.repairshop_email = request.POST.get("txt_email")
#         repairshop.repairshop_address = request.POST.get("txt_address")
#         repairshop.save()
#         return redirect('Repairshop:MyProfile')
#     return render(request, 'Repairshop/EditProfile.html', {'Repairshop': repairshop})

# # ChangePassword
# def ChangePassword(request):
#     repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#     dbpassword = repairshop.repairshop_password  # Fixed typo: repaiershop_password -> repairshop_password
#     if request.method == "POST":
#         old_password = request.POST.get("txt_old")
#         new_password = request.POST.get("txt_new")
#         retype_password = request.POST.get("txt_retype")
#         if dbpassword == old_password:
#             if new_password == retype_password:
#                 repairshop.repairshop_password = new_password  # Fixed: renter -> repairshop
#                 repairshop.save()
#                 return redirect('Repairshop:MyProfile')
#             else:
#                 return render(request, 'Repairshop/ChangePassword.html', {'msg': "Password mismatch"})
#         else:
#             return render(request, 'Repairshop/ChangePassword.html', {'msg': 'Invalid password'})
#     return render(request, 'Repairshop/ChangePassword.html')



# def update_repair_status(request, request_id, status):
#     try:
#         repair = tbl_repair.objects.get(id=request_id)
#         repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#         if repair.repairshop != repairshop:
#             raise Http404("You don’t have permission to update this request.")
        
#         if not repair.repairshop:
#             repair.repairshop = repairshop
#             repair.save()

#         valid_transitions = {
#             0: [1],    # Requested → Accepted
#             1: [3],    # Accepted → Picked Up
#             2: [0],    # Cancelled → Requested
#             3: [4],    # Picked Up → In Progress
#             4: [5],    # In Progress → Completed
#             5: [5, 9], # Completed → Set Amount or COD Requested
#             6: [7],    # Payment Completed → Delivered
#             7: [6, 8], # Delivered → Payment Completed (for COD) or Returned
#             9: [7],    # COD Requested → Delivered
#         }

#         if request.method == "POST":
#             if status == 5:  # Setting amount
#                 repair_amount = request.POST.get('repair_amount')
#                 if repair_amount:
#                     repair.repair_amount = repair_amount
#                     repair.repair_status = 5
#                     repair.save()
#                     messages.success(request, "Repair completed and amount set. Invoice generated.")
#                     return redirect('Repairshop:invoice', request_id=request_id)
#                 else:
#                     messages.error(request, "Please provide a repair amount.")
#             elif status == 1:  # Accepting with pickup date
#                 date_scheduled = request.POST.get('date_scheduled')
#                 if date_scheduled:
#                     repair.date_scheduled = date_scheduled
#                     repair.repair_status = 1
#                     repair.save()
#                     messages.success(request, "Repair request accepted with pickup date.")
#                 else:
#                     messages.error(request, "Please provide a pickup date.")
#             else:
#                 messages.error(request, "Invalid POST request for this status.")
#         elif repair.repair_status in valid_transitions and status in valid_transitions[repair.repair_status]:
#             repair.repair_status = status
#             repair.save()
#             if status == 9:
#                 messages.success(request, "COD requested by user.")
#             elif status == 7 and repair.repair_status == 9:
#                 messages.success(request, "Item delivered. Collect cash on delivery.")
#             elif status == 6 and repair.repair_status == 7:
#                 messages.success(request, "COD payment collected and completed.")
#             else:
#                 messages.success(request, f"Status updated to {status}.")
#         else:
#             messages.error(request, "Invalid status transition.")
#     except tbl_repair.DoesNotExist:
#         raise Http404("Repair request not found.")
#     return redirect('Repairshop:ViewRepairRequest')

# def edit_request(request, request_id):
#     try:
#         repair = tbl_repair.objects.get(id=request_id)
#         repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#         if repair.repairshop != repairshop:
#             raise Http404("You don’t have permission to edit this request.")
        
#         if request.method == "POST":
#             repair.device_details = request.POST.get('device_details')
#             repair.problem_details = request.POST.get('problem_details')
#             repair.pickup_address = request.POST.get('pickup_address')
#             repair.repair_notes = request.POST.get('repair_notes')
#             repair.save()
#             messages.success(request, "Repair details updated successfully.")
#             return redirect('Repairshop:view_repair_requests')
#         return render(request, 'Repairshop/EditRequest.html', {'repair': repair})
#     except tbl_repair.DoesNotExist:
#         raise Http404("Repair request not found.")

# def invoice(request, request_id):
#     try:
#         repair = tbl_repair.objects.get(id=request_id)
#         repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
#         if repair.repairshop != repairshop:
#             raise Http404("You don’t have permission to view this invoice.")
#         if repair.repair_status < 5:
#             raise Http404("Invoice not available yet.")
#         if not repair.repairshop:
#             messages.error(request, "No repair shop assigned to this request.")
#             return redirect('Repairshop:ViewRepairRequest')
#         return render(request, 'Repairshop/RepairInvoice.html', {'repair': repair})
#     except tbl_repair.DoesNotExist:
#         raise Http404("Repair request not found.")





# from django.shortcuts import render, redirect
# from django.db.models import Sum
# from django.contrib import messages
# from datetime import datetime
# from .models import tbl_repairshop, tbl_repair

# def SalesProfit(request):
#     try:
#         # Get the current repair shop from session
#         repairshop = tbl_repairshop.objects.get(id=request.session['sid'])
        
#         # Base queryset for completed repairs (statuses 6, 7, 8, 9)
#         completed_repairs = tbl_repair.objects.filter(
#             repairshop=repairshop,
#             repair_status__in=[6, 7, 8, 9]  # Card Payment Completed, Delivered COD, Returned, COD Payment Completed
#         ).order_by('-request_date')  # Latest first

#         # Handle date filter
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')
        
#         if start_date and end_date:
#             try:
#                 start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#                 end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#                 # Filter by date range (inclusive)
#                 completed_repairs = completed_repairs.filter(
#                     request_date__range=[start_date, end_date]
#                 )
#             except ValueError:
#                 messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
#         elif start_date or end_date:
#             messages.warning(request, "Please provide both start and end dates.")

#         # Calculate metrics
#         total_sales = completed_repairs.aggregate(total=Sum('repair_amount'))['total'] or 0
#         pending_cod_payments = completed_repairs.filter(repair_status=7).aggregate(total=Sum('repair_amount'))['total'] or 0
#         total_profit = total_sales  # Profit = sales (no costs tracked)
#         repair_count = completed_repairs.count()

#         # Prepare context
#         context = {
#             'repairshop': repairshop,
#             'total_sales': total_sales,
#             'pending_cod_payments': pending_cod_payments,
#             'total_profit': total_profit,
#             'repair_count': repair_count,
#             'repairs': completed_repairs
#         }
        
#         return render(request, "Repairshop/SalesProfit.html", context)
#     except tbl_repairshop.DoesNotExist:
#         messages.error(request, "Repair shop not found. Please log in.")
#         return redirect('Repairshop:login')
#     except KeyError:
#         messages.error(request, "Please log in to view sales and profit.")
#         return redirect('Repairshop:login')


# def chatpage(request,id):
#     user  = tbl_user.objects.get(id=id)
#     return render(request,"Repairshop/Chat.html",{"user":user})

# def ajaxchat(request):
#     from_repairshop = tbl_repairshop.objects.get(id=request.session["sid"])
#     to_user = tbl_user.objects.get(id=request.POST.get("tid"))
#     tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),repairshop_from=from_repairshop,user_to=to_user,chat_file=request.FILES.get("file"))
#     return render(request,"Renter/Chat.html")

# def ajaxchatview(request):
#     tid = request.GET.get("tid")
#     user = tbl_repairshop.objects.get(id=request.session["sid"])
#     chat_data = tbl_chat.objects.filter((Q(repairshop_from=user) | Q(repairshop_to=user)) & (Q(user_from=tid) | Q(user_to=tid))).order_by('chat_time')
#     return render(request,"Renter/ChatView.html",{"data":chat_data,"tid":int(tid)})

# def clearchat(request):
#     tbl_chat.objects.filter(Q(repairshop_from=request.session["sid"]) & Q(user_to=request.GET.get("tid")) | (Q(user_from=request.GET.get("tid")) & Q(repairshop_to=request.session["uid"]))).delete()
#     return render(request,"Renter/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})