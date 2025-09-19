from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """Crée et sauvegarde un User avec l'email et le mot de passe"""
        if not email:
            raise ValueError('email deja existant')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email, password=None, **extra_fields):
        """Crée un utilisateur normal"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    
    
    def create_superuser(self, email, password, **extra_fields):
        """Crée un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.EST_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    



class User(AbstractUser):
    # Add any additional fields you want for your user model
    EST_FORMATEUR = 'formateur'
    EST_APPRENTIS = 'apprentis'
    EST_ADMIN = 'admin'
    ROLE_CHOICES = [
        (EST_FORMATEUR, 'Formateur'),
        (EST_APPRENTIS, 'Apprenti'),
        (EST_ADMIN, 'Administrateur'),
    ]
    
    # Champ email doit être unique car c'est le USERNAME_FIELD
    email = models.EmailField(
        _('email address'),
        unique=True,  # Ceci est crucial
        error_messages={
            'unique': _("Un utilisateur avec cet email existe déjà."),
        }
    )
    role = models.CharField( max_length=20,  choices=ROLE_CHOICES, default=EST_APPRENTIS)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    
     # Utilisation de l'email comme identifiant principal
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    
    def __str__(self):
        return self.username
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_formateur(self):
        return self.role == self.EST_FORMATEUR
    
    def is_apprenti(self):
        return self.role == self.EST_APPRENTIS
    
    def is_admin(self):
        return self.role == self.EST_ADMIN