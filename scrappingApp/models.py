from django.db import models

class CarDetail(models.Model):
    carModel = models.CharField(max_length=200)
    carMileage = models.CharField(max_length=200)
    carRegistration = models.CharField(max_length=200)
    carPower = models.CharField(max_length=200)
    carGearbox = models.CharField(max_length=200)
    carEngine = models.CharField(max_length=200)
    carGears = models.CharField(max_length=200)
    carFuelType = models.CharField(max_length=200)
    carFuelConsumption = models.CharField(max_length=200)
    carEmissions = models.CharField(max_length=200)
    carColor = models.CharField(max_length=200)
    carManColor = models.CharField(max_length=200)
    carBodyType = models.CharField(max_length=200)
    carType = models.CharField(max_length=200)
    carSeats = models.CharField(max_length=50)
    carDoors = models.CharField(max_length=50)
    countryName = models.CharField(max_length=200)
    carOfferNumber = models.CharField(max_length=200)
    carModelCode = models.CharField(max_length=200)
    carPreviousOwner = models.CharField(max_length=200)
    carrEmissionClass = models.CharField(max_length=200)
    carNonSmoker = models.CharField(max_length=200)
    carPrice = models.CharField(max_length=200)
    carVAT = models.CharField(max_length=200)
    carEquipment = models.CharField(max_length=200)
    carContactName = models.CharField(max_length=200)
    carContactNumber = models.CharField(max_length=200)
    carContactAddress = models.CharField(max_length=200)
    carCompanyName = models.CharField(max_length=200)

    def __str__(self):
        return self.carModel

