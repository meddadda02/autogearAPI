from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    driver.get('https://occasion.kifal.ma/annonces')
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    
    cars = soup.find_all('div', class_='col-lg-6 col-md-6 col-xl-6') 
    print(f'Nombre de voitures trouvées: {len(cars)}')

    car_data = []

    for car in cars:
        link_element = car.find('a', href=True)
        link = link_element['href'] if link_element else None
        if link:
            full_link = link if link.startswith('http') else f'https://occasion.kifal.ma{link}'            
            if is_valid_url(full_link):
                try:
                    driver.get(full_link)
                    car_src = driver.page_source
                    car_soup = BeautifulSoup(car_src, 'lxml')
                    
                    # Extraire la marque et le modèle
                    title_element = car_soup.find('h1', {'class': 'h3 mb-2'})
                    if title_element:
                        title_text = title_element.text.strip()
                        brand, model = title_text.split(' ', 1)  # Sépare la marque et le modèle
                    else:
                        brand, model = None, None
                    
                    # Extraction year
                    year_element = car_soup.find('span', {'itemprop': 'productionYear'}).text.strip() if car_soup.find('span', {'itemprop': 'productionYear'}) else None
                    if year_element:
                        year = ''.join(filter(str.isdigit, year_element))
                        year = int(year) if year else None
                    else:
                        year = None 
                    
                    # Extraction hp        
                    hp_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-1')
                    for line in hp_element:
                        if 'Puissance fiscale' in line.text:
                            hp_text = line.find('span', {'class':'float-right'}).text.strip()
                            hp = ''.join(filter(str.isdigit, hp_text))
                            hp = int(hp) if hp else None
                            break
                    
                    # Extraction mileage
                    mileage_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-1')
                    for line in mileage_element:
                        if 'Kilométrage' in line.text:
                            mileage_text = line.find('span', {'class':'float-right'}).text.strip()
                            mileage = ''.join(filter(str.isdigit, mileage_text))
                            mileage = int(mileage) if mileage else None
                            break
                    
                    # Extraction cartype
                    cartype_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-1')
                    for line in cartype_element:
                        if 'Type de voiture' in line.text:
                            cartype_text = line.find('span', {'class':'float-right'}).text.strip()
                            # Extraire uniquement la première partie avant le /
                            if cartype_text:
                                cartype = cartype_text.split('/')[0].strip()
                            break
                    
                    # Extraction doors
                    doors = None
                    doors_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-2')
                    for line in doors_element:
                        if 'Nombre de portes' in line.text.strip():
                            doors_span = line.find_all('span')[1]  # Le deuxième <span> contient le nombre des portes
                            if doors_span:
                                doors_text = doors_span.text.strip()
                                doors = ''.join(filter(str.isdigit, doors_text))
                                doors = int(doors) if doors else None
                            break
                    
                    # Extraction seats   
                    seats = None
                    seats_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-2')
                    for line in seats_element:
                        if 'Nombre de places' in line.text.strip():
                            seats_span = line.find_all('span')[1]  # Le deuxième <span> contient le nombre des places
                            if seats_span:
                                seats_text = seats_span.text.strip()
                                seats = ''.join(filter(str.isdigit, seats_text))
                                seats = int(seats) if seats else None
                            break
                    
                    # Extraction gearbox
                    gearbox = None
                    gearbox_element = car_soup.find_all('div', class_='col-12 col-lg-6 mb-2')
                    for line in gearbox_element:
                        if 'Type boite vitesse' in line.text.strip():
                            gearbox_span = line.find_all('span')
                            gearbox_text = gearbox_span[1].text.strip()
                            if 'BVM' in gearbox_text:
                                gearbox = 'manual'
                            elif 'BVA' in gearbox_text:
                                gearbox = 'automatique'
                            break
                    
                    fuel = car_soup.find('p', {'itemprop': 'fuelType'}).text.strip() if car_soup.find('p', {'itemprop': 'fuelType'}) else None
                    
                    # Extraction garage  name     
                    parsed_url = urlparse(link)
                    garage = parsed_url.netloc

                    # Extraction images
                    images = []
                    img_elements = car_soup.find_all('img')
                    for img in img_elements:
                        img_url = img.get('src')
                        if img_url:
                            images.append(img_url)

                    car_info = {
                        "fuel": fuel,
                        "doors": doors,
                        "seats": seats,
                        "gearbox": gearbox,
                        "hp": hp,
                        "model": model, 
                        "brand": brand,
                        "year": year,
                        "cartype": cartype,
                        "mileage": mileage,
                        "garage": garage,
                        "images": images,
                    }
                    car_data.append(car_info)
                
                except Exception as e:
                    print(f'Erreur lors de l\'accès à l\'URL: {full_link}')
                    print(f'Exception: {e}')
                    continue
    
    json_output = json.dumps(car_data, ensure_ascii=False, indent=4)
    print(json_output)
    driver.quit()

main()
