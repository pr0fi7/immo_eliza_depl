from fastapi import FastAPI
from pydantic import BaseModel
import csv
import uvicorn
from predict import predict
from typing import Union


app = FastAPI()

class Item(BaseModel):
    nbr_frontages: int
    equipped_kitchen: str
    nbr_bedrooms: int
    latitude: float
    longitude: float
    total_area_sqm: float
    surface_land_sqm: Union[float, None]
    terrace_sqm: float
    garden_sqm: float
    province: str = None
    heating_type: str = None
    state_building: str = None
    property_type: str = None
    epc: str = None
    locality: str = None
    subproperty_type: str = None
    region: str = None
    fl_terrace: bool
    fl_garden: bool
    fl_swimming_pool: bool


    

@app.get("/")
async def root():
    return {"message": "alive"}

@app.post("/predict")
async def create_item(item: Item):
    with open("csv_file.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(item.__dict__().keys())
        writer.writerow(item.__dict__().values())
    print("hi")
    return predict("csv_file.csv")

if __name__ == "__main__":
    uvicorn.run("main_app:app", port=8000, host="0.0.0.0", reload=True)

