from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm,generalprofileform,sellerprofileform
from .models import GenralData,merchantprofile
from shop.models import Category
from django.urls import reverse_lazy

@login_required
def customerprofileview(request):
    userform=UserUpdateForm()
    profileform=generalprofileform()
    
    if request.method=="POST":
        userform=UserUpdateForm(request.POST,instance=request.user)
        profileform=generalprofileform(request.POST,request.FILES,instance=request.user.profile)
        
        if profileform.is_valid() and userform.is_valid():
            userform.save(commit=True)
            profileform.save(commit=True)
            return redirect('userprofile')
        else:
            userform=UserUpdateForm(instance=request.user)
            profileform=generalprofileform(instance=request.user.profile)
            

    return render(request,'account/customer_profile_create.html',{'profileform':profileform,'userform':userform})

class sellercreateview(LoginRequiredMixin,CreateView):
    model= merchantprofile
    form_class=sellerprofileform
    template_name='account/merchant_profile_create.html'
    success_url=reverse_lazy('userprofile')
    def form_valid(self,form):
        form.instance.user=self.request.user
        form.instance.id=self.request.user.id
        return super().form_valid(form)


class sellerupdateview(UpdateView):
    model=merchantprofile
    form_class=sellerprofileform
    template_name='account/merchant_profile_create.html'
    success_url=reverse_lazy('userprofile')

    def form_valid(self,form):
        return super().form_valid(form)

@login_required
def profile(request):
    obj=GenralData.objects.get(user=request.user)
    if obj:
        print('present')
        #obj1=merchantprofile.objects.get(user=request.user)
    try:
        obj1=merchantprofile.objects.get(user=request.user)
        print(obj1.skill)
        if obj1:
            print('seller')
        return render(request,'account/profile.html',{'obj':obj,'obj12':obj1})
    except:
        print('cus')
    return render(request,'account/profile.html',{'obj':obj})
    #return render(request,'profile.html',{'obj':obj,'obj1':obj1})