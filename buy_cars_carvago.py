from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import re

service = Service(ChromeDriverManager().install())             
driver = webdriver.Chrome(service=service)

def main():
    driver.get('https://carvago.com/cars')
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    cars = soup.find_all('div', {'data-testid': 'feature.car.card'})
    print(f'Nombre de voitures trouvées: {len(cars)}')

    car_data = []
    for car in cars:
        link = car.find('a')['href'] if car.find('a') else None

        if link:
            link = f'https://carvago.com{link}'
            
            driver.get(link)

            car_src = driver.page_source
            car_soup = BeautifulSoup(car_src, 'lxml')
            brand = car_soup.find('div', {'class': 'css-4lpo8k'}).text.strip() if car_soup.find('div', {'class': 'css-4lpo8k'}) else None
            fuel = car_soup.find('div', {'data-testid': 'desc-fuel-type'}).text.strip() if car_soup.find('div', {'data-testid': 'desc-fuel-type'}) else None
            gearbox = car_soup.find('div', {'class': 'css-1wcsshc'}).text.strip() if car_soup.find('div', {'class': 'css-1wcsshc'}) else None
            
            year_element = car_soup.find('div', {'data-testid': 'desc-registration-date'}).text.strip() if car_soup.find('div', {'data-testid': 'desc-registration-date'}) else None
            if year_element:
                year = ''.join(filter(str.isdigit, year_element))
                year = int(year) if year else None
            else:
                year = None 
                
            price_element = car_soup.find('div', {'class': 'css-gg4vpm'}).text.strip() if car_soup.find('div', {'class': 'css-gg4vpm'}) else None
            if price_element:
                price = ''.join(filter(str.isdigit, price_element))
                price = int(price) if price else None
            else:
                price = None 
                
            mealage_element = car_soup.find('div', {'data-testid': 'desc-mileage'}).text.strip() if car_soup.find('div', {'data-testid': 'desc-mileage'}) else None
            if mealage_element:
                mealage = ''.join(filter(str.isdigit, mealage_element))
                mealage = int(mealage) if mealage else None
            else:
                mealage = None

            hp_element = car_soup.find('div', {'class': 'css-15rm72b'}).text.strip() if car_soup.find('div', {'class': 'css-15rm72b'}) else None         
            if hp_element:
                hp = ''.join(filter(str.isdigit, hp_element))
                hp = int(hp) if hp else None
            else:
                hp = None
            
            doors_element = None
            for p in car_soup.find_all('p', {'class': 'chakra-text'}):
                if "doors" in p.text.lower():
                    doors_element = p.find_next('div').text.strip() if p.find_next('div') else None
                    break
            
            if doors_element:
                doors = re.search(r'\d+', doors_element)
                doors = int(doors.group(0)) if doors else None
            else:
                doors = None 
            
            seats = None
            seats_element = None
            for p in car_soup.find_all('p', {'class': 'chakra-text'}):
                if 'seats' in p.text.lower():  
                    seats_element = p.find_next('div').text.strip() if p.find_next('div') else None                    
                    if seats_element:
                        seats = ''.join(filter(str.isdigit, seats_element))  # Extrait uniquement les chiffres
                        seats = int(seats) if seats else None  # Convertit en entier s'il y a des chiffres
                    break
            cartype = None
            for p in car_soup.find_all('p', {'class': 'chakra-text'}):
                if "body" in p.text.lower() and "color" not in p.text.lower():
                    cartype_div = p.find_next('div')
                    if cartype_div:
                        cartype = cartype_div.text.strip()
                    break
            
            marque = None
            for p in car_soup.find_all('p', {'class': 'chakra-text'}):
                if "model" in p.text.lower():
                    marque = p.find_next('div').text.strip() if p.find_next('div') else None
                    break
                
            images = []
            img_elements = car_soup.find_all('img')
            for img in img_elements:
                img_url = img.get('src')
                if img_url:
                    images.append(img_url)
             
            parsed_url = urlparse(link)
            garage = parsed_url.netloc
            
            car_info = {
                "brand": brand,
                "marque": marque,
                "garage": garage,
                "fuel": fuel,
                "gearbox": gearbox,
                "year": year,
                "price": price,
                "mealage": mealage,
                "hp": hp,
                "doors": doors,
                "seats": seats,
                "cartype": cartype,
                "images": images,
            }
            car_data.append(car_info)

    json_output = json.dumps(car_data, ensure_ascii=False, indent=4)
    print(json_output)

    driver.quit()

main()
