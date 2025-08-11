
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from detection.models import Customer  # Import your Customer model
from djoser.signals import user_registered
User = get_user_model()
@receiver(user_registered)
def create_customer(sender, user, request, **kwargs):
    phone = request.data.get('phone')
    city = request.data.get('city')
    gender=request.data.get('gender')
    role = request.data.get('role')
    bio=request.data.get('bio')
    image = request.data.get('image')
    Customer.objects.create(
        user=user,
        phone=phone,
        city=city,
        gender=gender,
        role=role,
        bio=bio,
        image=image
    )





