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
            make = request.POST['cmake']
            model = request.POST.get('cmodel', False)
            cartype = request.POST['cartype']

            fromprices = request.POST['fromprice']
            toprice = request.POST['toprice']

            reg = request.POST['registration']

            mileage = request.POST['mileage']

            engine_type = request.POST['engine_type']

            frompower = request.POST['frompower']
            topower = request.POST['topower']

            sort_id = request.POST["sort_by"]
            country_list = request.POST.getlist('country', "germany")
            maximum_target = request.POST['max_cat']

            if model:
                result = CarDetail.objects.filter(
                        Q(carModel__contains=make.lower()) & Q(carModel__contains=model.lower())
                        & Q(carType__contains=cartype.lower()) & Q(countryName__contains=country_list[0].lower()) &
                        Q(carRegistration__lte=reg) & Q(carMileage__lte=mileage)
                    ).values(
                        "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                        "carFuelType", "carImage",
                        "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                        "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                        "carNonSmoker",
                        "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                        "carCompanyName")
            else:
                result = CarDetail.objects.filter(
                    Q(carModel__contains=make.lower())
                    & Q(carType__contains=cartype.lower()) & Q(countryName__contains=country_list[0].lower()) &
                    Q(carRegistration__lte=reg) & Q(carMileage__lte=mileage)
                ).values(
                    "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                    "carFuelType", "carImage",
                    "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                    "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                    "carNonSmoker",
                    "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                    "carCompanyName")

            if sort_id == "1":
                result = sorted(result, key=lambda d: d['carPrice'])
            elif sort_id == "2":
                result = sorted(result, key=lambda d: d['carPrice'], reverse=True)
            elif sort_id == "3":
                result = sorted(result, key=lambda d: d['carMileage'])
            elif sort_id == "4":
                result = sorted(result, key=lambda d: d['carMileage'], reverse=True)
            elif sort_id == "5":
                result = sorted(result, key=lambda d: d['carRegistration'])
            elif sort_id == "6":
                result = sorted(result, key=lambda d: d['carRegistration'], reverse=True)
            else:
                result = result


            if result:
                return render(request, "index.html",
                              {"result": result, "models_name": modelNameList, "model_values": model_values,
                               "max_target": maximum_target})
            else:
                result = CarDetail.objects.filter(
                    Q(carModel__contains=make.lower())
                     & Q(countryName__contains=country_list[0].lower())
                ).values(
                    "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                    "carFuelType", "carImage",
                    "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType", "carSeats",
                    "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner", "carrEmissionClass",
                    "carNonSmoker",
                    "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                    "carCompanyName")
                if result:
                    msg = "Other Related Data"
                    return render(request, "index.html",
                                  {"result": result, "msg": msg,  "models_name": modelNameList,
                                   "model_values": model_values,
                                   "max_target": maximum_target})
                else:
                    msg = "Not Found Data"
                    return render(request, "index.html",
                                  {"result": result, "msg": msg, "models_name": modelNameList,
                                   "model_values": model_values, "max_target": maximum_target})

    except:
        msg = "Bad Request Error"
        return render(request, "index.html",
                      {"msg": msg, "models_name": modelNameList, "model_values": model_values})