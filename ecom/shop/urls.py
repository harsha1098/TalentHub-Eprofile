from django.conf.urls import url
from shop import views
app_name='shop'


urlpatterns=[
    url('^about/$',views.about,name='about'),
    url('^buy/$',views.buy,name='buy'),
    url(r'^creategig/',views.Merchant_GigCreateView.as_view(),name='gigcreate'),
    url(r'^seller_giglist/',views.Merchant_Giglist.as_view(),name='giglist'),
    url(r'^gig/(?P<gigs_pk>\d+)/update/',views.Merchant_Gigupdate.as_view(),name='gigupdate'),
    url(r'^gig/(?P<pk>\d+)/$',views.Merchant_Gigdetail.as_view(),name='seller_gigdetail'),
    url(r'^gig/(?P<pk>\d+)/delete/',views.Merchant_Gigdelete.as_view(),name='gigdelete'),
        
    url(r'^charge/(?P<id>\d+)/(?P<amt>\d+)', views.charge, name='charge'),
    url(r'^gig/(?P<gig_id>\d+)/sendmessage',views.message_create.as_view(),name='message_create'),
    url(r'^gig/(?P<gig_id>\d+)/(?P<token>\w+)',views.transaction_update,name='transaction-update'),
    url(r'^gig/message',views.message_view,name='message_view'),

    url(r'^(?P<gig_id>\d+)',views.gigdetail.as_view(),name='gigdetail'),

    url(r'^subcat/(?P<maincat>\w+)/$',views.category_sublist.as_view(),name='sublist'),

    url(r'^(?P<maincat>\w+)/(?P<slug>\w+)/sellerlist',views.gig_sellerlist.as_view(),name='gigsellerlist'),

    
    
    
    
    
    url('^',views.home,name='home'),
    
]