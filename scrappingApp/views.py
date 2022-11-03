from django.db.models import Q
from django.shortcuts import render
# from script_files.main import *

from .models import CarDetail

# modelNumbList, modelNameList = getMakeModel()

modelNameList = ['Audi', 'BMW', 'Ford', 'Mercedes-Benz', 'Opel', 'Volkswagen', 'Renault', '9ff', 'Abarth',
                 'AC', 'ACM', 'Acura', 'Aiways', 'Aixam', 'Alba Mobility', 'Alfa Romeo', 'Alpina', 'Alpine',
                 'Amphicar', 'Angelelli Automobili', 'Ariel Motor', 'Artega', 'Aspid', 'Aston Martin', 'Austin',
                 'Austin-Healey', 'Autobianchi', 'Baic', 'BAIC', 'Bedford', 'Bellier', 'Bentley', 'Boldmen', 'Bolloré',
                 'Borgward', 'Brilliance', 'Bristol', 'Bugatti', 'Buick', 'BYD', 'Cadillac', 'Caravans-Wohnm', 'Carver',
                 'Casalini', 'Caterham', 'Changhe', 'Chatenet', 'Chery', 'Chevrolet', 'Chrysler', 'Citroen', 'CityEL',
                 'Corvette', 'Cupra', 'Dacia', 'Daewoo', 'DAF', 'Daihatsu', 'Daimler', 'Dangel', 'De la Chapelle',
                 'De Tomaso', 'Delorean', 'Devinci Cars', 'DFSK', 'Dodge', 'Donkervoort', 'DR Motor', 'DS Automobiles',
                 'Dutton', 'e.GO', 'Econelo', 'Edran', 'Elaris', 'Embuggy', 'EMC', 'Estrima', 'Evetta', 'EVO', 'Ferrari',
                 'Fiat', 'FISKER', 'Gac Gonow', 'Galloper', 'Gappy', 'GAZ', 'GEM', 'GEMBALLA', 'Genesis', 'Giana', 'Gillet',
                 'Giotti Victoria', 'GMC', 'Goupil', 'Great Wall', 'Grecav', 'GTA', 'Haima', 'Hamann', 'Haval', 'Holden',
                 'Honda', 'HUMMER', 'Hurtan', 'Hyundai', 'Ineos', 'Infiniti', 'Innocenti', 'Iso Rivolta', 'Isuzu', 'Iveco',
                 'IZH', 'JAC', 'Jaguar', 'Jeep', 'Jensen', 'Karma', 'Kia', 'Koenigsegg', 'KTM', 'Lada', 'Lamborghini',
                 'Lancia', 'Land Rover', 'LDV', 'LEVC', 'Lexus', 'Lifan', 'Ligier', 'Lincoln', 'Linzda', 'Lorinser',
                 'Lotus', 'Lucid', 'Lynk & Co', 'Mahindra', 'MAN', 'Mansory', 'Martin', 'Martin Motors', 'Maserati',
                 'Maxus', 'Maybach', 'Mazda', 'McLaren', 'Mega', 'Melex', 'Mercury', 'MG', 'Microcar', 'Militem', 'Minari',
                 'Minauto', 'MINI', 'Mitsubishi', 'Mitsuoka', 'Morgan', 'Moskvich', 'MP Lafer', 'MPM Motors', 'Nissan',
                 'NSU', 'Oldsmobile', 'Oldtimer', 'Pagani', 'Panther Westwinds', 'Peugeot', 'PGO', 'Piaggio', 'Plymouth',
                 'Polestar', 'Pontiac', 'Porsche', 'Proton', 'Puch', 'RAM', 'Regis', 'Reliant', 'Rolls-Royce', 'Rover',
                 'Ruf', 'Saab', 'Santana', 'SEAT', 'Segway', 'Selvo', 'Seres', 'Sevic', 'SGS', 'Shelby', 'Shuanghuan',
                 'Singer', 'Skoda', 'smart', 'SpeedArt', 'Spyker', 'SsangYong', 'StreetScooter', 'Studebaker', 'Subaru',
                 'Suzuki', 'Talbot', 'Tasso', 'Tata', 'Tazzari EV', 'TECHART', 'Tesla', 'Town Life', 'Toyota', 'Trabant',
                 'Trailer-Anhänger', 'Triumph', 'Trucks-Lkw', 'TVR', 'UAZ', 'Vanden Plas', 'Vanderhall', 'VAZ', 'VEM',
                 'VinFast', 'Volvo', 'Wartburg', 'Weltmeister', 'Wenckstern', 'Westfield', 'Wiesmann', 'XBus', 'XEV',
                 'Zastava', 'ZAZ', 'Zhidou', 'Zotye', 'Others']
def index(request):
    return render(request, 'index.html', {"models_name":modelNameList})

def result(request):
    if request.method == "POST":
        model = request.POST['type'].lower()

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

        result = CarDetail.objects.filter(
                Q(carModel__contains=model) & Q(countryName__contains=country) &
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
            return render(request, "index.html",
                          {"result": result, "models_name": modelNameList})
        else:
            result = CarDetail.objects.filter(
                Q(carModel__contains=model)).values(
                "carModel", "carMileage", "carRegistration", "carPower", "carGearbox", "carEngine", "carGears",
                "carFuelType",
                "carFuelConsumption", "carEmissions", "carColor", "carManColor", "carBodyType", "carType",
                "carSeats",
                "carDoors", "countryName", "carOfferNumber", "carModelCode", "carPreviousOwner",
                "carrEmissionClass",
                "carNonSmoker",
                "carPrice", "carVAT", "carEquipment", "carContactName", "carContactNumber", "carContactAddress",
                "carCompanyName")
            if not result:
                result = ""
            return render(request, "index.html",
                          {"result": result, "models_name": modelNameList})