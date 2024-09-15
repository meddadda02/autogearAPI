from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def main():
        driver.get('https://www.moteur.ma/fr/voiture/achat-voiture-occasion/')
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        
        cars = soup.find_all('div', class_='row-item row-item-checkout link') 
        print(f'Nombre de voitures trouvées: {len(cars)}')

        car_data = []
        for car in cars:            
            link_element = car.find('a', href=True)
            link = link_element['href'] if link_element else None
            if link:
                    # Assure-toi que le lien est complet
                    full_link = link if link.startswith('http') else f'https://www.moteur.ma{link}'
                    driver.get(full_link)
                    car_src = driver.page_source
                    car_soup = BeautifulSoup(car_src, 'lxml')

                            # Extraire la marque et le modèle
                                        # Extraction du titre
                    title_element = car_soup.find('h3', {'class': 'title_mark_model'})
                    if title_element:
                        title_text = title_element.text.strip()
                        if ' ' in title_text:
                            brand, model = title_text.split(' ', 1)  # Sépare la marque et le modèle
                        else:
                            brand, model = title_text, None
                    else:
                        brand, model = None, None

                    # Extraction du prix
                    price_element = car_soup.find('div', {'class': 'color_primary text_bold price-block'})
                    if price_element:
                        price_text = price_element.text.strip()
                        price = ''.join(filter(str.isdigit, price_text))
                        price = int(price) if price else None
                    else:
                        price = None

                    # Extraction de l'année
                    year = None
                    year_element = car_soup.find_all('div', class_='detail_line')
                    for line in year_element:
                        if 'Année' in line.text:
                            year_text = line.find('span', class_='text_bold').text.strip()
                            year = ''.join(filter(str.isdigit, year_text))
                            year = int(year) if year else None
                            break

                    # Extraction du kilométrage
                    mileage = None
                    mileage_element = car_soup.find_all('div', class_='detail_line')
                    for line in mileage_element:
                        if 'Kilométrage' in line.text:
                            mileage_text = line.find('span', class_='text_bold').text.strip()
                            mileage = ''.join(filter(str.isdigit, mileage_text))
                            mileage = int(mileage) if mileage else None
                            break

                    # Extraction de la boîte de vitesses
                    gearbox = None
                    gearbox_element = car_soup.find_all('div', class_='detail_line')
                    for line in gearbox_element:
                        if 'Boite de vitesses' in line.text:
                            gearbox_text = line.find('span', class_='text_bold').text.strip()
                            gearbox = gearbox_text if gearbox_text else None
                            break

                    # Extraction du carburant
                    fuel = None
                    fuel_element = car_soup.find_all('div', class_='detail_line')
                    for line in fuel_element:
                        if 'Carburant' in line.text:
                            fuel_text = line.find('span', class_='text_bold').text.strip()
                            fuel = fuel_text if fuel_text else None
                            break

                    # Extraction du type de carrosserie
                    cartype = None
                    cartype_element = car_soup.find_all('div', class_='detail_line')
                    for line in cartype_element:
                        if 'Carrosserie' in line.text:
                            cartype_text = line.find('span', class_='text_bold').text.strip()
                            if cartype_text:
                                cartype = cartype_text.split('et')[0].strip()
                            break

                    # Extraction de la puissance fiscale
                    hp = None
                    hp_element = car_soup.find_all('div', class_='detail_line')
                    for line in hp_element:
                        if 'Puissance fiscale' in line.text:
                            hp_text = line.find('span', class_='text_bold').text.strip()
                            hp = ''.join(filter(str.isdigit, hp_text))
                            hp = int(hp) if hp else None
                            break

                    # Extraction du nombre de portes
                    doors = None
                    doors_element = car_soup.find_all('div', class_='detail_line')
                    for line in doors_element:
                        if 'Nombre de portes' in line.text:
                            doors_text = line.find('span', class_='text_bold').text.strip()
                            doors = ''.join(filter(str.isdigit, doors_text))
                            doors = int(doors) if doors else None
                            break

                    # Extraction du nom du site (garage)
                    parsed_url = urlparse(link)
                    garage = parsed_url.netloc  # Récupère le nom de domaine

                    # Extraction des images
                    images = []
                    img_elements = car_soup.find_all('img')  # Trouver toutes les balises <img>
                    for img in img_elements:
                        img_url = img.get('src')
                        if img_url:
                            images.append(img_url)
                    car_info = {
                        "price": price,
                        "brand":brand,
                        "model":model,
                        "year": year,
                        "mileage":mileage,
                        "gearbox":gearbox,
                        "fuel":fuel,
                        "hp":hp,
                        "doors":doors,
                        "cartype":cartype,
                        "garage":garage,
                        "images":images
                    }
                    car_data.append(car_info)

        json_output = json.dumps(car_data, ensure_ascii=False, indent=4)
        print(json_output)
        driver.quit()

main()
