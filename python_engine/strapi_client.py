import requests
import os
from dotenv import load_dotenv

load_dotenv()

STRAPI_URL = os.getenv("STRAPI_URL", "http://localhost:1337")
STRAPI_API_TOKEN = os.getenv("STRAPI_API_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {STRAPI_API_TOKEN}"
}

def upload_image_to_strapi(filepath):
    """
    Uploads an image to Strapi's Media Library.
    Returns the media ID if successful, otherwise None.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    url = f"{STRAPI_URL}/api/upload"
    try:
        with open(filepath, 'rb') as f:
            files = {'files': (os.path.basename(filepath), f, 'image/jpeg')}
            response = requests.post(url, headers={"Authorization": HEADERS["Authorization"]}, files=files)
            
        if response.status_code in [200, 201]:
            data = response.json()
            media_id = data[0]['id']
            print(f"Image uploaded successfully. Media ID: {media_id}")
            return media_id
        else:
            print(f"Failed to upload image. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def create_city(name_tr, country_tr, shortinfo_tr, name_en, country_en, shortinfo_en):
    """
    Creates a City in Strapi in TR (default) and EN locales.
    Returns the TR and EN City documentIds.
    """
    url = f"{STRAPI_URL}/api/cities"
    
    city_id_tr = None
    city_id_en = None
    

    payload_tr = {"data": {"Name": name_tr, "Country": country_tr, "ShortInfo": shortinfo_tr, "publishedAt": "2024-01-01T00:00:00.000Z"}}
    try:
        response = requests.post(url, headers=HEADERS, json=payload_tr)
        if response.status_code in [200, 201]:
            city_id_tr = response.json()['data']['documentId']
            print(f"Created City (TR): {name_tr}")
        else:
            print(f"Failed to create City (TR). Response: {response.text}")
    except Exception as e:
        print(f"Error creating TR city: {e}")
        

    payload_en = {"data": {"Name": name_en, "Country": country_en, "ShortInfo": shortinfo_en, "publishedAt": "2024-01-01T00:00:00.000Z"}}
    try:
        loc_response = requests.post(f"{url}?locale=en", headers=HEADERS, json=payload_en)
        if loc_response.status_code in [200, 201]:
            city_id_en = loc_response.json()['data']['documentId']
            print(f"Created City (EN): {name_en}")
        else:
            print(f"Failed to create City (EN). Response: {loc_response.text}")
    except Exception as e:
        print(f"Error creating EN city: {e}")
            
    return city_id_tr, city_id_en

def create_place(name_tr, description_tr, rating, city_id_tr, city_id_en, media_id, name_en, description_en):
    """
    Creates a Place in Strapi in TR and EN locales.
    """
    url = f"{STRAPI_URL}/api/places"
    

    if city_id_tr:
        payload_tr = {"data": {"Name": name_tr, "Description": description_tr, "Rating": rating, "city": city_id_tr, "publishedAt": "2024-01-01T00:00:00.000Z"}}
        if media_id: payload_tr["data"]["CoverImage"] = media_id
            
        try:
            response = requests.post(url, headers=HEADERS, json=payload_tr)
            if response.status_code in [200, 201]:
                print(f"Created Place (TR): {name_tr}")
            else:
                print(f"Failed to create Place (TR). Response: {response.text}")
        except Exception as e:
            print(f"Error creating TR place: {e}")
            

    if city_id_en:
        payload_en = {"data": {"Name": name_en, "Description": description_en, "Rating": rating, "city": city_id_en, "publishedAt": "2024-01-01T00:00:00.000Z"}}
        if media_id: payload_en["data"]["CoverImage"] = media_id
            
        try:
            loc_response = requests.post(f"{url}?locale=en", headers=HEADERS, json=payload_en)
            if loc_response.status_code in [200, 201]:
                print(f"Created Place (EN): {name_en}")
            else:
                print(f"Failed to create Place (EN). Response: {loc_response.text}")
        except Exception as e:
            print(f"Error creating EN place: {e}")

if __name__ == "__main__":
    pass
