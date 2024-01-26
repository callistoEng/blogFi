from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.base_user import BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Set a valid email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_content_creator', True)
        extra_fields.setdefault('is_regular', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    class UserTypes(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        CONTENT_CREATOR = "CONTENT_CREATOR", "Content_creator"
    # base_type = UserTypes.REGULAR
    username = None
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    is_content_creator = models.BooleanField(default=False)
    is_regular = models.BooleanField(default=True)
    journalist_ref_code = models.CharField(max_length=20, blank=True, null=True)
    is_verified_journalist = models.BooleanField(default=False)
    news_agency_name = models.CharField(max_length=200, blank=True, null=True)
    user_name = models.CharField(verbose_name="User Name", max_length=200, blank=True, null=True)
    about_me = models.CharField(verbose_name="About Me", max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='Images/profile_img/', verbose_name='Profile Image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=15, blank=True, null=True)
    content_creator_name = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'mobile_phone','content_creator_name','is_content_creator','news_agency_name','about_me',
        'is_regular', 'user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True,blank=True)
    created_at = models.DateField(default=now) 
    property_trend = models.BooleanField(blank=True, null=True)
    market_economy = models.BooleanField(blank=True, null=True)
    investment_property = models.BooleanField(blank=True, null=True)
    infrustructure = models.BooleanField(blank=True, null=True)
    is_land = models.BooleanField(blank=True, null=True)
    tax_legal = models.BooleanField(blank=True, null=True)
    quickSale = models.BooleanField(blank=True, null=True)
    is_opinion = models.BooleanField(blank=True, null=True)
    has_preferences = models.BooleanField(blank=True, null=True)
    others = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        verbose_name = 'Preference'
        verbose_name_plural = 'Preferences'

    def __str__(self):
        return "user preferences"

class NewsLetterSubscription(models.Model):
    class SubscriptionTypes(models.TextChoices):
        FREE = "FREE", "Free" 
        PREMIUM = "PREMIUM", "Premium"
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True,blank=True)
    email = models.EmailField(blank=False, null=False, unique=True, max_length=80)
    created_at = models.DateTimeField(default=now)
    is_subscribed = models.BooleanField(default=False)
    subscription_type = models.CharField(choices=SubscriptionTypes.choices, max_length=30, blank=True, null=True, default=SubscriptionTypes.FREE)
    
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
    def __str__(self):
        return f"{self.subscription_type} subscription"

class ClientRating(models.Model):
    COMMENT_STATE = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="Rater")
    rating = models.PositiveIntegerField(default=3)
    guest_user = models.CharField(max_length=40,blank=True, null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="AgentRated")
    user_comment = models.CharField(max_length=200,blank=True, null=True)
    status = models.CharField(max_length=5, choices=COMMENT_STATE, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)




