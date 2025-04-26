from django.urls import path
from Repairshop import views
app_name="Repairshop"

urlpatterns = [
     path('RepairshopHomepage/',views.RepairshopHomepage,name="RepairshopHomepage"),
     path('ViewRepairRequest/',views.ViewRepairRequest,name="ViewRepairRequest"),
     path('reject/<int:reid>',views.reject,name='reject'),
     path('RequestForm/<int:id>',views.RequestForm,name="RequestForm"),
     

     path('MyProfile/',views.MyProfile,name="MyProfile"),
     path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
     path('EditProfile/',views.EditProfile,name="EditProfile"),
     
     path('request/<int:request_id>/update/', views.update_request, name='update_request'),
     path('request/<int:request_id>/revert/', views.revert_cancellation, name='revert_cancellation'),
     path('request/<int:request_id>/edit/', views.edit_request, name='edit_request'),

     path('Logout/',views.Logout,name='Logout'),


     path('update_repair_status/<int:request_id>/<int:status>/', views.update_repair_status, name='update_repair_status'),
     path('invoice/<int:request_id>/', views.invoice, name='invoice'),

     path('sales-profit/', views.SalesProfit, name='SalesProfit'),

     path('chatpager/<int:id>', views.chatpager, name="chatpager"),
     path('ajaxchatr/', views.ajaxchatr, name="ajaxchatr"),
     path('ajaxchatviewr/', views.ajaxchatviewr, name="ajaxchatviewr"),
     path('clearchatr/', views.clearchatr, name="clearchatr"),
]
