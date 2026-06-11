import requests
import urllib.parse
import os

def generate_image_for_place(place_name_en, city_name_en, output_dir="temp_images"):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    prompt = f"Professional travel photography of {place_name_en} in {city_name_en}, sunny day, clear sky, highly detailed, 4k resolution"
    encoded_prompt = urllib.parse.quote(prompt)
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    filename = f"{place_name_en.replace(' ', '_')}_{city_name_en.replace(' ', '_')}.jpg".lower()
    filepath = os.path.join(output_dir, filename)
    
    print(f"Generating image for {place_name_en}...")
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Image saved to {filepath}")
            return filepath
        else:
            print(f"Failed to generate image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

if __name__ == "__main__":
    generate_image_for_place("Eiffel Tower", "Paris")
