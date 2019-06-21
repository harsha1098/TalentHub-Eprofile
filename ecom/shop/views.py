from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views .generic import ListView,DetailView,TemplateView
from .forms import gigform,message_form
from django.urls import reverse_lazy
from .models import Gigs,Category,MessageModel
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Category,Gigs,Transaction
from accounts.models import merchantprofile
from django.core.exceptions import PermissionDenied
import stripe
from django.conf import settings
from django.utils import timezone
import uuid
from django.contrib.auth.decorators import login_required 


def home(request):
    cat=Category.CATEGORY_CHOICES

    return render(request,'account/home.html',{'cat':cat})

def about(request):
    return render(request,'shop/about.html')

def buy(request):
    cat=Category.CATEGORY_CHOICES
    return render(request,'categories.html',{'cat':cat})

#for merchant
class Merchant_GigCreateView(CreateView):
    form_class=gigform
    template_name='shop/merchant/gigform.html'
    success_url=reverse_lazy('userprofile')

    def form_valid(self,form):
        form.save(commit=False)
        form.instance.user=self.request.user
        form.save()
        return super().form_valid(form)

class Merchant_Giglist(ListView):
    model=Gigs
    template_name='shop/merchant/seller-gigs.html'
    def get_queryset(self):
        obj=Gigs.objects.filter(user=self.request.user)
        return obj

class Merchant_Gigdetail(DetailView):
    model=Gigs
    template_name='shop/merchant/seller_gigdetail.html'

    def get_context_data(self,**kwargs):
        # gig_id=self.kwargs.get(kwargs['pk'])
        context={}
        context['obj']=Gigs.objects.get(pk=self.kwargs.get('pk'))
        return context

class Merchant_Gigupdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Gigs
    form_class=gigform
    pk_url_kwarg='gigs_pk'
    template_name='shop/merchant/gigform.html'
    context_object_name='gig'
    success_url=reverse_lazy('shop:gigdetail')
    def form_valid(self,form):
        form.instance.user=self.request.user
        gig=form.save()
        return redirect('shop:seller_gigdetail',pk=gig.pk)
        return super().form_valid(form)
    def test_func(self):
        gig=self.get_object()
        if self.request.user==gig.user:
            return True
        else:
            return False


   
        

class Merchant_Gigdelete(DeleteView,LoginRequiredMixin):
    model=Gigs
    success_url=reverse_lazy('shop:giglist')
    template_name='shop/merchant/confirm_delete.html'

    def form_valid(self,**kwargs):
        if method=="POST" :
            obj=get_object_or_404(Gigs,id=pk)
            if  form.is_valid and obj.user==self.request.user:
                obj.delete()
                return redirect(reverse('shop:giglist'))
            else:
                raise PermissionDenied

        else:
            return redirect('shop:giglist')
            



class category_sublist(TemplateView):
    model=Category
    template_name='shop/customer/subcat_list.html'
    def get_context_data(self,**kwargs):
        all_obj=Category.objects.all()
        context=super(category_sublist,self).get_context_data(**kwargs)
        context['main_cat']=Category.CATEGORY_CHOICES
        context['sub_cat']=Category.objects.filter(parent=self.kwargs.get('maincat'))
        context['all']=all_obj
        print(Category.objects.filter(parent=self.kwargs.get('maincat')))
        return context

    
class gig_sellerlist(TemplateView):
    model=Gigs
    template_name='shop/customer/gig_seller.html'
    

    def get_context_data(self,**kwargs):
        context=super(gig_sellerlist,self).get_context_data(**kwargs)
        context['main_cat']=Category.CATEGORY_CHOICES
        cat=Category.objects.get(slug=self.kwargs.get('slug'))
        context['cat']=cat
        context['obj']=Gigs.objects.filter(category=cat)
        return context
    # def get_queryset(self,**kwargs):
    #     obj=Gigs.objects.filter(category=Category.objects.get(slug=self.kwargs.get('slug')))
    #     print(obj)
    #     return obj

class gigdetail(TemplateView):
    model=Gigs
    template_name='shop/customer/gigdetail.html'

    def get_context_data(self,**kwargs):
        gig=Gigs.objects.get(id=self.kwargs.get('gig_id'))
        amt=(gig.price+2)*100
        context=super(gigdetail,self).get_context_data(**kwargs)
        context['gig_obj']=gig
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['amt']=amt
        return context




stripe.api_key = settings.STRIPE_SECRET_KEY

def charge(request,id,amt): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=amt,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        
        context={'token':request.POST['stripeToken'],'amt':int(amt)/100,'obj':id}
        return render(request, 'charge.html',context)


    
class message_create(CreateView):
    form_class=message_form
    template_name='shop/messageform.html'
    success_url=reverse_lazy('shop:gigdetail')

    def get(self, request, *args, **kwargs):
        context = {'form': message_form()}
        return render(request,'message_form.html',context)

    def post(self,request,**kwargs):
        gig=Gigs.objects.get(id=kwargs['gig_id'])
        mform=message_form(request.POST)
        if mform.is_valid():
            form=mform.save(commit=False)
            form.gig=gig
            form.sender=self.request.user
            form.reciever=gig.user
            form.save()
            return redirect('shop:home')
        return render(request,'message_form.html')




def message_view(request):
    msg=MessageModel.objects.filter(reciever=request.user)
    return render(request,'view_message.html',{'msg_obj':msg})

@login_required
def transaction_update(request,token,gig_id):
    token=token
    gig_obj=Gigs.objects.get(id=gig_id)
    orderid=str(uuid.uuid4())
    p=Transaction(gig=gig_obj,buyer=request.user,token=token,time=timezone.now(),amount=gig_obj.price,seller=gig_obj.user,order_id=orderid)
    p.save()
    return redirect('shop:message_create',gig_id)





    