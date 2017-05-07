from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)


class Horse(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)


class Motorcycle(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)


class House(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)


class Liquor(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)


class Ration(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)
