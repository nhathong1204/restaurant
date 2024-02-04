from django.urls import path
from . import views
from accounts import views as AccountView

urlpatterns = [
    path('', AccountView.vendorDashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
]
