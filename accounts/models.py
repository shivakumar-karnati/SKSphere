from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_pic = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField( blank=True )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username