import os
import requests
from dotenv import load_dotenv

load_dotenv('c:/Users/Berat Genç/Desktop/IY_proj2/python_engine/.env')
url = 'http://localhost:1337/api/cities?locale=all'
headers = {'Authorization': 'Bearer ' + str(os.getenv('STRAPI_API_TOKEN'))}
r = requests.get(url, headers=headers)
print("Status:", r.status_code)
print("Data:", r.json())
