from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
                                        BaseUserManager,
                                        AbstractBaseUser,
                                        )


class AllUser(BaseUserManager):
    def create_user(self, phone, email, password=None, first_name=None, last_name=None, **kwargs):
        if not email:
            raise ValueError("Need Email")
        
        if not phone:
            raise ValueError("Need Phone")
        
        if not first_name:
            raise ValueError("Need Name")
        
        if not last_name:
            raise ValueError("Need Surname")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = False
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    numbers      = RegexValidator(r'^[0-9a]*$', message='')
    phone        = models.CharField(max_length=11, unique=True, validators=[numbers])
    email        = models.EmailField(unique=True, max_length=244)
    first_name   = models.CharField(max_length=30, null=True, blank=True)
    last_name    = models.CharField(max_length=50, null=True, blank=True)
    is_active    = models.BooleanField(default=False, null=False)
    is_staff     = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    @property
    def fullName(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.phone}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    email      = models.EmailField()
    phone      = models.CharField(max_length=11)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name  = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user} {self.phone}"
