from django.db import models
from django.contrib.auth.models import User
from shop.models import Category
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

class GenralData(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    avatar=models.ImageField(default=r"C:\Users\Cybertron\Desktop\vision\TalentHub\static\img\desk.png",upload_to='profile_pics')
    is_customer=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


@receiver(user_signed_up)
def create_profile(sender, **kwargs):
    p=GenralData(user=kwargs['user'])
    p.save()


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

class merchantprofile(models.Model):
    CATEGORY_CHOICES = (
        ("GD", "Graphics & Design"),
        ("DM", "Digital & Marketing"),
        ("VA", "Video & Animation"),
        ("MA", "Music & Audio"),
        ("PT", "Programming & Tech")
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='merchant_profile')
    category=models.CharField(max_length=2,choices=CATEGORY_CHOICES)
    education=models.TextField()
    skill=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    is_merchant=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
# user.merchant_profile.Categ.objects.get(parent=user.merchan_profile.category)