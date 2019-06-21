"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from accounts import views as acc_views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/profile/',acc_views.profile,name='userprofile'),
    
    url(r'^accounts/', include('allauth.urls')),
    

    ##profile related##
    
    url(r'^create_customer_profile/',acc_views.customerprofileview,name='update_user_profile'),
    url(r'^create_merchant_profile/',acc_views.sellercreateview.as_view(),name='create_seller'),
    url(r'^(?P<pk>\d+)/update_merchant_profile/',acc_views.sellerupdateview.as_view(),name='update_profile'),

    url(r'^',include('shop.urls')),
     
]
