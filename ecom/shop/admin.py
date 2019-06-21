from django.contrib import admin
from .models import Category,Gigs,MessageModel

admin.site.register(Category)
admin.site.register(Gigs)
admin.site.register(MessageModel)