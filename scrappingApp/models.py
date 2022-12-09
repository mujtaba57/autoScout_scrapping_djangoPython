from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models import Q
class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).lower()


class CarDetail(models.Model):
    carModel = models.CharField(max_length=500)
    carImage = models.TextField()
    carMileage = models.CharField(max_length=500)
    carRegistration = models.CharField(max_length=500)
    carPower = models.CharField(max_length=500)
    carGearbox = models.CharField(max_length=500)
    carEngine = models.CharField(max_length=500)
    carGears = models.CharField(max_length=500)
    carFuelType = models.CharField(max_length=500)
    carFuelConsumption = models.CharField(max_length=500)
    carEmissions = models.CharField(max_length=500)
    carColor = models.CharField(max_length=500)
    carManColor = models.CharField(max_length=500)
    carBodyType = models.CharField(max_length=500)
    carType = models.CharField(max_length=500)
    carSeats = models.CharField(max_length=500)
    carDoors = models.CharField(max_length=500)
    countryName = models.CharField(max_length=500)
    carOfferNumber = models.CharField(max_length=500)
    carModelCode = models.CharField(max_length=500)
    carPreviousOwner = models.CharField(max_length=500)
    carrEmissionClass = models.CharField(max_length=500)
    carNonSmoker = models.CharField(max_length=500)
    carPrice = models.CharField(max_length=500)
    carVAT = models.CharField(max_length=500)
    carEquipment = models.TextField()
    carContactName = models.CharField(max_length=500)
    carContactNumber = models.CharField(max_length=500)
    carContactAddress = models.CharField(max_length=500)
    carCompanyName = models.CharField(max_length=500)

    def __str__(self):
        return self.carModel

class CarDataIndex(models.Model):
    nameIndex = models.TextField(default="Data Scraped Index")
    queryIndex = models.IntegerField(default=0)
    modify_time = models.DateTimeField()

    def __str__(self):
        return self.nameIndex

class DataScrapTime(models.Model):
    nameIndex = models.TextField(
        default="This time refers to the start and end, the execution time to scrape car detail data")
    startTime = models.TimeField()
    endTime = models.TimeField()

class CarLink(models.Model):
    carlinks = models.TextField()

    def __str__(self):
        return self.carlinks

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['carlinks'], name='carlinks')
    #     ]

class LinksIndex(models.Model):
    nameIndex = models.TextField(default="Car link Scrapped Index")
    yearQueryIndex = models.IntegerField(default=0)
    priceQueryIndex = models.IntegerField(default=0)
    carNameQueryIndex = models.IntegerField(default=0)
    modify_time = models.DateTimeField()

    def __str__(self):
        return self.nameIndex



class LinkScrapTime(models.Model):
    nameIndex = models.TextField(
        default="This time refers to the start and end, the execution time to scrape car links")

    startTime = models.TimeField()
    endTime = models.TimeField()