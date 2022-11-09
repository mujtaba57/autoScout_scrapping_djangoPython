from models import CarDetail
import pandas as pd

df = pd.read_csv("../scrappingApp/allCarInfo1000.csv")

for i in range(0, len(df)):
    CarDetail.objects.create(
        carModel=df['Unnamed: 0'][i], carMileage=df['mileage'][i], carRegistration=df['first registration'][i],
        carPower=df['power'][i], carImage=df['image'][i],
        carGearbox=df['gearbox'][i], carEngine=df['engine size'][i], carGears=df['gears'][i], carFuelType=df['fuel type'][i],
        carFuelConsumption=df['fuel consumption'][i], carEmissions=df['co₂-emissions'][i],
        carColor=df['colour'][i], carManColor=df['manufacturer colour'][i], carBodyType=df['body type'][i], carType=df['type'][i],
        carSeats=df['seats'][i], carDoors=df['doors'][i], countryName=df['country version'][i],
        carOfferNumber=df['offer number'][i], carModelCode=df['model code'][i], carPreviousOwner=df['previous owner'][i],
        carrEmissionClass=df['emission class'][i], carNonSmoker=df['non-smoker vehicle'][i],
        carPrice=df['price'][i], carVAT=df['VAT'][i], carEquipment=df['equipment'][i], carContactName=df['contact_name'][i],
        carContactNumber=df['contact_number'][i], carContactAddress=df['contact_address'][i],
        carCompanyName=df['company_name'][i]
    )


