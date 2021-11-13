from django.db import models
from django.contrib.auth.models import User


class Charity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RequestFund(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=500, blank=True)
    chariti = models.ForeignKey(Charity, on_delete=models.CASCADE)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Donor(models.Model):
    donor = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(max_length=500, default="")
    chariti = models.ForeignKey(Charity, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    ready_to_donate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.chariti)

class Donation_list(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    amount = models.CharField(max_length=100, default='NA')
    email = models.EmailField(max_length=100)
    chariti = models.ForeignKey(Charity, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)