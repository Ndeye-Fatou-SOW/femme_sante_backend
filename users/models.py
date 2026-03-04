# from django.db import models

# # Create your models here.


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid


class UserManager(BaseUserManager):
    """Gestionnaire personnalisé pour créer des utilisatrices"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisatrice principal"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisatrice'


class UserProfile(models.Model):
    """Profil détaillé de l'utilisatrice"""
    CONTRACEPTION_CHOICES = [
        ('pill', 'Pilule'), ('iud', 'Stérilet'), ('condom', 'Préservatif'),
        ('implant', 'Implant'), ('patch', 'Patch'), ('none', 'Aucune'), ('other', 'Autre'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    height = models.FloatField(null=True, blank=True)       # Taille en cm
    weight = models.FloatField(null=True, blank=True)       # Poids en kg
    avg_cycle_length = models.IntegerField(default=28)      # Durée cycle en jours
    avg_period_length = models.IntegerField(default=5)      # Durée règles en jours
    contraception_method = models.CharField(max_length=20, choices=CONTRACEPTION_CHOICES, default='none')
    medical_conditions = models.TextField(blank=True)
    preferences = models.JSONField(default=dict)
    notification_enabled = models.BooleanField(default=True)
    fcm_token = models.TextField(blank=True)               # Pour notifications push
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.user.email}"

    class Meta:
        db_table = 'user_profiles'
