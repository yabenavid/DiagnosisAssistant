from django.db import models

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name