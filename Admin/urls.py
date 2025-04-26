from django.urls import path
from Admin import views
app_name="Admin"

urlpatterns = [
    path("District/",views.District, name="District"),
    path('deletedistrict/<int:did>',views.DeleteDistrict,name="DeleteDistrict"),
    path('Editdistrict/<int:eid>',views.EditDistrict,name="EditDistrict"),

    path("Category/",views.Category, name="Category"),
    path('deletecategory/<int:did>',views.DeleteCategory,name="DeleteCategory"),
    path('Editcategory/<int:eid>',views.EditCategory,name="EditCategory"),

    path("Admin/",views.Admin, name="Admin"),
    path('deleteadmin/<int:did>',views.DeleteAdmin,name="DeleteAdmin"),
    path("Brand/",views.Brand,name="Brand"),
    path('deletebrand/<int:did>',views.DeleteBrand,name="DeleteBrand"),
    path("Type/",views.Type,name="Type"),
    path('deletetype/<int:did>',views.DeleteType,name="DeleteType"),

    path("Place/",views.Place,name="Place"),
    path('deleteplace/<int:did>',views.DeletePlace,name="DeletePlace"),
    path('Editplace/<int:eid>',views.EditPlace,name="EditPlace"),

    path("Subcategory/",views.Subcategory,name="Subcategory"),
    path('deletesubcategory/<int:did>',views.DeleteSubcategory,name="DeleteSubcategory"),
    path('Editsubcategory/<int:eid>',views.EditSubcategory,name="EditSubcategory"),


    path("Subtype/",views.Subtype,name="Subtype"),
    # Department
    path("Department/",views.Department,name="Department"),
    path('deletedepartment/<int:did>',views.DeleteDepartment,name="DeleteDepartment"),
    path('Editdepartment/<int:eid>',views.EditDepartment,name="EditDepartment"),

    # Designation
    path("Designation/",views.Designation,name="Designation"),
    path('deletedesignation/<int:did>',views.DeleteDesignation,name="DeleteDesignation"),
    path('Editdesignation/<int:eid>',views.EditDesignation,name="EditDesignation"),

    # Staff
    path("Staff/",views.Staff,name="Staff"),
    path('deletestaff/<int:did>',views.DeleteStaff,name="DeleteStaff"),
    path('Editstaff/<int:eid>',views.EditStaff,name="EditStaff"),

    # RenterApproval
    path('RenterApproval/',views.RenterApproval,name="RenterApproval"),
    path('acceptr/<int:acid>',views.acceptr,name='acceptr'),
    path('rejectr/<int:reid>',views.rejectr,name='rejectr'),

    #ViewUsers
    path('ViewUsers/',views.ViewUsers,name="ViewUsers"),
    path('ViewRepairshop/',views.ViewRepairshop,name="ViewRepairshop"),

    #ViewRenters
    path('ViewRenters/',views.ViewRenters,name="ViewRenters"),
    path('ViewProducts/',views.ViewProducts,name="ViewProducts"),
    path('ViewComplaints/',views.ViewComplaints,name="ViewComplaints"),
    path('ViewFeedbacks/',views.ViewFeedbacks,name="ViewFeedbacks"),

    #AddReply
    path('AddReply/<int:id>',views.AddReply,name="AddReply"),

    #Approve Repairshop
    path('RepairshopApproval/',views.RepairshopApproval,name="RepairshopApproval"),
    path('accept/<int:acid>',views.accept,name='accept'),
    path('reject/<int:reid>',views.reject,name='reject'),

    #AdminHomepage
    path('AdminHomepage/',views.AdminHomepage,name="AdminHomepage"),

    #Booking-Details
    path('booking_detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('transactions/', views.all_transactions, name='transactions'),
    path('RepairTransactions/', views.repair_transactions, name='RepairTransactions'),

    #Logout
    path('Logout/',views.Logout,name="Logout"),
]
