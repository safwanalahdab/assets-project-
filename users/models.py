from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="employees",
    )
    is_it_staff = models.BooleanField(default=False)
