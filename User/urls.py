from django.urls import path, include
from User import views
app_name = "User"

urlpatterns = [


    path('Homepage/', views.Homepage, name="Homepage"),
    path('Myprofile/', views.Myprofile, name="Myprofile"),
    path('Changepassword/', views.Changepassword, name="Changepassword"),
    path('Editprofile/', views.Editprofile, name="Editprofile"),


    path('AddProduct/', views.AddProduct, name="AddProduct"),
    path('DeleteAddProduct/<int:did>', views.DeleteAddProduct, name="DeleteAddProduct"),
    path('ViewProducts/', views.ViewProducts, name="ViewProducts"),


    path('AddStock/<int:did>', views.AddStock, name="AddStock"),


    path('Gallery/<int:id>/', views.Gallery, name="Gallery"),
    path('DeleteGallery/<int:did>', views.DeleteGallery, name="DeleteGallery"),
    path('ProductGallery/<int:id>/', views.ProductGallery, name="ProductGallery"),
    
    path('Complaint/<int:id>', views.Complaint, name="Complaint"),
    path('DeleteComplaint/<int:did>/', views.DeleteComplaint, name="DeleteComplaint"),


    path('Feedback/', views.Feedback, name="Feedback"),
    path('DeleteFeedback/<int:did>/', views.DeleteFeedback, name="DeleteFeedback"),

    path('Addcart/<int:pid>', views.Addcart, name='Addcart'),
    path('Mycart/', views.Mycart, name='Mycart'),
    path('DelCart/<int:did>', views.DelCart, name="delcart"),
    path('CartQty/', views.CartQty, name="cartqty"),


    path('Bookdetails/', views.Bookdetails, name="Bookdetails"),
    path('MyBooking/', views.MyBooking, name="MyBooking"),

    path('MyRentals/', views.MyRentals, name="MyRentals"),

    path('ViewRepairshop/', views.ViewRepairshop, name="ViewRepairshop"),
    path('RequestRepair/<int:rid>', views.RequestRepair, name="RequestRepair"),
    path('MyRepairRequests/', views.MyRepairRequests, name="MyRepairRequests"),
    
    path('AjaxSearch/', views.AjaxSearch, name="AjaxSearch"),
    path('Invoice/<int:id>/', views.Invoice, name="Invoice"),


    path('chatpage/<int:id>', views.chatpage, name="chatpage"),
    path('ajaxchat/', views.ajaxchat, name="ajaxchat"),
    path('ajaxchatview/', views.ajaxchatview, name="ajaxchatview"),
    path('clearchat/', views.clearchat, name="clearchat"),


    path('chatpageu/<int:id>', views.chatpageu, name="chatpageu"),
    path('ajaxchatu/', views.ajaxchatu, name="ajaxchatu"),
    path('ajaxchatviewu/', views.ajaxchatviewu, name="ajaxchatviewu"),
    path('clearchatu/', views.clearchatu, name="clearchatu"),



    path('rating/<int:mid>', views.rating, name="rating"),
    path('ajaxstar/', views.ajaxstar, name="ajaxstar"),
    path('starrating/', views.starrating, name="starrating"),


    path("payment/<int:pid>", views.payment, name="payment"),
    path('loader/', views.loader, name='loader'),
    path('paymentsuc/', views.paymentsuc, name='paymentsuc'),


    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.ViewProducts, name='view_products'),
    path('productdetails/', views.ProductDetails, name='ProductDetails'),


    path('repair/<int:repair_id>/cancel/', views.cancel_repair_request, name='cancel_repair_request'),
   
    path('ordercancel/<int:id>',views.ordercancel,name='ordercancel'),
    path('Logout/',views.Logout,name='Logout'),

    
    path('RepairPayment/<int:repair_id>/', views.RepairPayment, name='RepairPayment'),
    path('RepairInvoice/<int:repair_id>/', views.RepairInvoice, name='RepairInvoice'),
      
    path('ProductBookings/', views.ProductBookings, name='ProductBookings'),

    path('ViewBooking/', views.ViewBooking, name='ViewBooking'),
    path('updatests/<int:cart_id>/<int:status>/', views.updatests, name='updatests'),



    path('chatpager/<int:id>', views.chatpager, name="chatpager"),
    path('ajaxchatr/', views.ajaxchatr, name="ajaxchatr"),
    path('ajaxchatviewr/', views.ajaxchatviewr, name="ajaxchatviewr"),
    path('clearchatr/', views.clearchatr, name="clearchatr"),
]
