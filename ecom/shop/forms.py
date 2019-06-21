from django import forms
from .models import Gigs
from .models import Category,MessageModel
from django.contrib.auth.models import User

class gigform(forms.ModelForm):
    # category_choice=Category.objects.all(parent=request.user.merchant_profile.category)
    # category=forms.ChoiceField(choices=category_choice)

    class Meta:
        model=Gigs
        fields=('title','category','description','price','photo')

class message_form(forms.ModelForm):
	class Meta:
		model=MessageModel
		fields=('title','msg')


