from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Хранит определение моделей, которые описывают используемые в приложении данные
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Хэширование пароля
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель представляющая пользователей.
    
    Атрибуты:
        name -- имя пользователя
        phone_number -- номер телефона пользователя
        role -- роль пользователя
        password -- пароль пользователя (хэширован)
        email -- электронная почта пользователя
    """
    
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    ]
    
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(max_length=255, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class ServiceProvider(models.Model):
    """
    Модель представляющая представителя услуги.
    
    Атрибуты:
        user -- связь с моделью User
        service_name -- название услуги
        description -- описание услуги
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'service_provider'})
    service_name = models.CharField(max_length=255)
    description = models.TextField()


class Service(models.Model):
    """
    Модель представляющая услуги.
    
    Атрибуты:
        provider -- представитель услуги, оказывающий данную услугу
        name -- название услуги
        duration -- продолжительность услуги в минутах
    """
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()  

class Schedule(models.Model):
    """
    Модель представляющая расписание.
    
    Атрибуты:
        provider -- представитель услуги
        date -- дата
        start_time -- время начала свободного слота
        end_time -- время окончания свободного слота
    """
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    
class Appointment(models.Model):
    """
    Модель представляющая запись на услугу.
    
    Атрибуты:
        user -- пользователь, который записался на услугу
        service -- услуга, на которую записался пользователь
        schedule -- расписание, к которому привязана запись
        start_time -- время начала записи
        end_time -- время окончания записи
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

