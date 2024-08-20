import requests as rq

BASE = "http://127.0.0.1:5000/"

response = rq.get(url=BASE + "Car_Brands", 
                  json={'name':'chevrolet impala'})

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")