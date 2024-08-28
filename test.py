import requests as rq

BASE = "http://127.0.0.1:5000/"

rqs= {
    0 : {'id': 510, 'name': 'Seat Ibiza', 'year': 2010, 'cylinders': 4, 'origin': 'germany', 'weight': 1200, 'horsepower': 70},
    1 : {'displacement': 1997, 'name': 'bmw m3', 'cylinders': 6, 'acceleration': 7.5, 'weight': 1600, 'horsepower': 170},
    2 : {'name': 'VW Polo', 'year': 2004, 'cylinders': 3, 'origin': 'germany', 'weight': 900, 'horsepower': 67}
}
for i in range(3):
    response = rq.post(url=BASE + "Car_Brands/add_model", json=rqs[i])

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

response = rq.get(url=BASE + "Car_Brands/retrieve_models", json=rqs[2])

if response.status_code == 200:
    data = response.json()
    for item in data:
        print(item)
else:
    print(f"Error: {response.status_code} - {response.text}")

response = rq.delete(url=BASE + "Car_Brands/delete_model", json={'id':512})

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")

response = rq.get(url=BASE + "Year_Comparison/year_range", json={'model_year_1': 75, 'model_year_2': 76})

if response.status_code == 200:
    data = response.json()
    for item in data:
        print(item)
else:
    print(f"Error: {response.status_code} - {response.text}")