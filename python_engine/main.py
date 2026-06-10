import os
from scraper import scrape_travel_data
from ai_generator import generate_image_for_place
from strapi_client import upload_image_to_strapi, create_city, create_place

def main():
    print("--- Starting AI-Powered Travel Guide Automation ---")
    
    # 1. Scrape and translate data
    cities_data = scrape_travel_data()
    
    if not cities_data:
        print("No data scraped. Exiting.")
        return

    # 2. Process each city
    for city in cities_data:
        print(f"\nProcessing City: {city['Name']}")
        
        # Create city in Strapi
        city_id_tr, city_id_en = create_city(
            name_tr=city['Name'],
            country_tr=city['Country'],
            shortinfo_tr=city['ShortInfo'],
            name_en=city.get('Name_en', city['Name']),
            country_en=city.get('Country_en', city['Country']),
            shortinfo_en=city.get('ShortInfo_en', city['ShortInfo'])
        )
        
        if not city_id_tr:
            print(f"Skipping places for {city['Name']} due to city creation failure.")
            continue
            
        # 3. Process each place in the city
        for place in city['Places']:
            print(f"\n  Processing Place: {place['Name']}")
            
            # Generate AI Image
            image_path = generate_image_for_place(
                place_name_en=place.get('Name_en', place['Name']),
                city_name_en=city.get('Name_en', city['Name'])
            )
            
            media_id = None
            if image_path:
                # Upload to Strapi
                media_id = upload_image_to_strapi(image_path)
                
            # Create place in Strapi
            create_place(
                name_tr=place['Name'],
                description_tr=place['Description'],
                rating=place.get('Rating', 4.5),
                city_id_tr=city_id_tr,
                city_id_en=city_id_en,
                media_id=media_id,
                name_en=place.get('Name_en', place['Name']),
                description_en=place.get('Description_en', place['Description'])
            )
            
    print("\n--- Automation Completed Successfully ---")

if __name__ == "__main__":
    main()
