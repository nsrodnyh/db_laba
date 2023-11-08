from django.db import models


class LastName(models.Model):
    last_name = models.CharField(max_length=20, unique=True)


class FirstName(models.Model):
    first_name = models.CharField(max_length=20, unique=True)


class Patronymic(models.Model):
    patronymic = models.CharField(max_length=30, unique=True)


class Street(models.Model):
    street = models.CharField(max_length=50, unique=True)


class Main(models.Model):
    last_name = models.ForeignKey('LastName', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.ForeignKey('FirstName', on_delete=models.SET_NULL, null=True)
    patronymic = models.ForeignKey('Patronymic', on_delete=models.SET_NULL, null=True, blank=True)
    street = models.ForeignKey('Street', on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(null=True)
    building = models.CharField(max_length=4, null=True)
    apartment = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=14)
