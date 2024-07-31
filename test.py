import requests as rq

BASE = "http://127.0.0.1:5000/"

response = rq.put(url=BASE + "Car_Brands/bmw", json={'year': 2000, 'acceleration': 100})

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")