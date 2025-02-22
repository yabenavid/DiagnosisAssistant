from django.db import models
from django.contrib.auth.models import AbstractUser
from managementhospital.models import Hospital
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    second_last_name = models.CharField(max_length=60)
    specialism = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.last_name}"

class Belong(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)