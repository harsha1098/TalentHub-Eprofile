from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from .models import GenralData,merchantprofile

class MyCustomSignupForm(SignupForm):
	email=forms.EmailField()

	# class Meta:
	# 	fields=('username','email','password1','password2')

	def save(self,request):
		user=super(MyCustomSignupForm,self).save(request)

		email=self.cleaned_data['email']
		return user


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email')

class generalprofileform(forms.ModelForm):
    class Meta:
        model=GenralData
        fields=('avatar',)

class sellerprofileform(forms.ModelForm):
    class Meta:
        model=merchantprofile
        exclude=('user','is_merchant')