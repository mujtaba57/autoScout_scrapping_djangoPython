from django.db.models import Q
from django.shortcuts import render, redirect
from .models import CarDetail
import json
import pandas as pd

with open('csv_files/carModelName.json', 'r') as f:
  data = json.load(f)

model_values = data["model_data"]
modelNameList = list(data["model_data"].keys())

def index(request):
    return render(request, 'index.html', {"models_name":modelNameList, "model_values": model_values})

def result(request):
    try:
        if request.method == "POST":
            make = request.POST['cmake'].lower()
            model = request.POST['cmodel'].lower()
            cartype = request.POST['cartype'].lower()

            fromprices = request.POST['fromprice']
            toprice = request.POST['toprice']

            fromfr = request.POST['fromfr']
            tofr = request.POST['tofr']

            frommile = request.POST['frommile']
            tomile = request.POST['tomile']

            engine_type = request.POST['engine_type']

            frompower = request.POST['frompower']
            topower = request.POST['topower']

            sort_id = request.POST["sort_by"]
            country_list = request.POST['country[]'].lower()
            maximum_target = int(request.POST['max_cat'])

            if model:
                result = CarDetail.objects.filter(
                        Q(carModel__contains=make) & Q(carModel__contains=model) & Q(countryName__contains=country_list)
                        & Q(carType__contains=cartype) &
                        Q(carRegistration__range=(fromfr, tofr)) & Q(carMileage__range=(frommile, tomile))
                    ).values(
                        "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                        "carFuelType",
                        "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                        "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                        "carNonSmoker",
                        "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                        "carCompanyName")
            else:
                result = CarDetail.objects.filter(
                    Q(carModel__contains=make) & Q(countryName__contains=country_list)
                    & Q(carType__contains=cartype) &
                    Q(carRegistration__range=(fromfr, tofr)) & Q(carMileage__range=(frommile, tomile))
                ).values(
                    "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                    "carFuelType",
                    "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                    "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                    "carNonSmoker",
                    "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                    "carCompanyName")

            if result:
                if sort_id == "1":
                    result = sorted(result, key=lambda d: d['carPrice'], reverse=True)
                elif sort_id ==  "2":
                    result = sorted(result, key=lambda d: d['carPrice'], reverse=False)
                elif sort_id ==  "3":
                    result = sorted(result, key=lambda d: d['carMileage'], reverse=True)
                elif sort_id ==  "4":
                    result = sorted(result, key=lambda d: d['carMileage'], reverse=False)
                elif sort_id ==  "5":
                    result = sorted(result, key=lambda d: d['carRegistration'], reverse=True)
                elif sort_id ==  "6":
                    result = sorted(result, key=lambda d: d['carRegistration'], reverse=False)
                print(result)
                if len(result) > maximum_target:
                    return render(request, "index.html",
                                  {"result": result[0:maximum_target], "models_name": modelNameList, "model_values": model_values})
                else:
                    return render(request, "index.html",
                                  {"result": result, "models_name": modelNameList, "model_values": model_values})
            else:
                result = ""
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "model_values": model_values})
    except Exception as e:
        return render(request, "index.html",
                      {"result": e.args[0], "models_name": modelNameList, "model_values": model_values})