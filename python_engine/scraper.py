import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def scrape_travel_data():
    """
    Scrapes sample travel data from a source (e.g., Wikipedia) and translates descriptions to English.
    Returns a list of cities and their places.
    """
    print("Scraping sample data...")
    
    cities_data = [
        {
            "Name": "Istanbul",
            "Country": "Turkey",
            "ShortInfo": "Tarihi ve kültürel zenginlikleriyle Asya ve Avrupa'yı birbirine bağlayan eşsiz bir şehir.",
            "Places": [
                {
                    "Name": "Ayasofya",
                    "Description": "Bizans döneminden kalma tarihi bir cami ve müze. Eşsiz mimarisiyle dikkat çeker.",
                    "Rating": 4.9
                },
                {
                    "Name": "Galata Kulesi",
                    "Description": "İstanbul manzarasına hakim tarihi kule. Cenevizliler tarafından inşa edilmiştir.",
                    "Rating": 4.7
                }
            ]
        },
        {
            "Name": "Paris",
            "Country": "France",
            "ShortInfo": "Aşkın ve ışığın şehri. Modanın, sanatın ve kültürün başkenti.",
            "Places": [
                {
                    "Name": "Eyfel Kulesi",
                    "Description": "Paris'in ve Fransa'nın sembolü olan demir kule.",
                    "Rating": 4.8
                },
                {
                    "Name": "Louvre Müzesi",
                    "Description": "Dünyanın en büyük ve en ünlü sanat müzelerinden biri.",
                    "Rating": 4.9
                }
            ]
        }
    ]

    translator = GoogleTranslator(source='tr', target='en')

    print("Translating data to English...")
    for city in cities_data:
        try:
            city['Name_en'] = translator.translate(city['Name'])
            city['Country_en'] = translator.translate(city['Country'])
            city['ShortInfo_en'] = translator.translate(city['ShortInfo'])
            
            for place in city['Places']:
                place['Name_en'] = translator.translate(place['Name'])
                place['Description_en'] = translator.translate(place['Description'])
        except Exception as e:
            print(f"Translation error: {e}")
            city['Name_en'] = city['Name']
            city['Country_en'] = city['Country']
            city['ShortInfo_en'] = city['ShortInfo']
            for place in city['Places']:
                place['Name_en'] = place['Name']
                place['Description_en'] = place['Description']

    print("Scraping and translation completed.")
    return cities_data

if __name__ == "__main__":
    data = scrape_travel_data()
    print(data)
