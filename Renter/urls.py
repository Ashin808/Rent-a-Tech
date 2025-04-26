from django.urls import path
from Renter import views
app_name="Renter"

urlpatterns = [
     path('RenterHomePage/',views.RenterHomePage,name="RenterHomePage"),
     path('MyProfile/',views.MyProfile,name="MyProfile"),
     path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
     path('EditProfile/',views.EditProfile,name="EditProfile"),

     path('AddProduct/',views.AddProduct,name="AddProduct"),
     path('DeleteAddProduct/<int:did>',views.DeleteAddProduct,name="DeleteAddProduct"),
     path('AjaxSubcategory/',views.AjaxSubcategory,name="AjaxSubcategory"),

     path('AddStock/<int:id>  ',views.AddStock,name="AddStock"),
     path('Gallery/<int:id>',views.Gallery,name="Gallery"),
     path('DeleteGallery/<int:did>',views.DeleteGallery,name="DeleteGallery"),

     path('ViewComplaints/',views.ViewComplaints,name="ViewComplaints"),
     path('ViewBooking/',views.ViewBooking,name="ViewBooking"),

      path('updatests/<int:id>/<int:sts>',views.updatests,name="updatests"),


      path('chatpage/<int:id>',views.chatpage,name="chatpage"),
      path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
      path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
      path('clearchat/',views.clearchat,name="clearchat"),

      path('Logout/',views.Logout,name="Logout"),
      path('SalesProfits/', views.SalesProfits, name='SalesProfits'),
      

]
