from statistics import mode
from django.db import models

# Create your models here.
class Weather(models.Model):
    dates = models.DateField()
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    precipitation = models.IntegerField()


class Corn_grain_yield(models.Model):
    year = models.CharField(max_length=7)
    harvested = models.BigIntegerField()


class DataAnalysis(models.Model):
    year=models.CharField(max_length=7)
    max_temp_avg= models.FloatField()
    min_temp_avg = models.FloatField()
    total_precipitation = models.FloatField()

