from django.db.models import Q
from django.shortcuts import render
from script_files.main import *

from .models import CarDetail

modelNumbList, modelNameList = getMakeModel()

def index(request):
    return render(request, 'index.html', {"models_name":modelNameList, "models_num": modelNumbList})

def result(request):
    if request.method == "POST":
        model = request.POST['type']

        fromprices = request.POST['fromprice']
        toprice = request.POST['toprice']

        fromfr = request.POST['fromfr']
        tofr = request.POST['tofr']

        frommile = request.POST['frommile']
        tomile = request.POST['tomile']

        engine_type = request.POST['engine_type']

        frompower = request.POST['frompower']
        topower = request.POST['topower']

        country = request.POST['country'].lower()

        if model != "" and fromprices != "" and toprice != "" and fromfr != "" and tofr != "" and frommile \
                != "" and tomile != "" and engine_type != "" and frompower != "" and topower != "" and country != "":
            result = CarDetail.objects.filter(
                Q(carModel__contains=model) & Q(carPrice__range=(fromprices, toprice)) &
                Q(carRegistration__range=(fromfr, tofr)) & Q(carMileage__range=(frommile, tomile)) &
                Q(carPower__range=(frompower, topower)) & Q(carFuelType__contains=engine_type) &
                Q(countryName__contains=country)
            ).values(
                "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                "carFuelType",
                "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                "carNonSmoker",
                "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                "carCompanyName")
            if result:
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "models_num": modelNumbList})
            else:
                result = ''
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "models_num": modelNumbList})
        else:
            result = CarDetail.objects.filter(
                Q(carModel__contains=model) & Q(carFuelType__contains=engine_type) &
                Q(countryName__contains=country)
            ).values(
                "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                "carFuelType",
                "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                "carNonSmoker",
                "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                "carCompanyName")
            if result:
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "models_num": modelNumbList})
            else:
                result = ''
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "models_num": modelNumbList})
