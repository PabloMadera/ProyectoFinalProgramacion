import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

#en cada una de las funciones aunque parezca repitivo me genera un cvs sin el error de la ultima clase
def webscrapingRegion():
    driver = ChromeDriverManager().install()
    service = Service(driver)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get('https://www.wikidex.net/wiki/WikiDex')

    txtBuscador = navegador.find_element(By.NAME, 'search')
    btnIr = navegador.find_element(By.NAME, 'go')

    txtBuscador.send_keys('región')

    try:
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, 'go')))
        btnIr.click()
    except ElementClickInterceptedException:
        navegador.execute_script("arguments[0].click();", btnIr)

    time.sleep(3)

    region = []
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    items = soup.find_all('li', {'class': 'toclevel-2'})

    for item in items:
        toctext = item.find('span', {'class': 'toctext'}).text.strip()
        region.append({'Nombre': toctext})

    navegador.quit()
    df = pd.DataFrame(region)
    df.to_csv('region.csv', index=False)
    return df


def webscrapingPokedex():
    driver_path = ChromeDriverManager().install()
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=Service(driver_path), options=options)
    navegador.get('https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon')

    time.sleep(5)

    html = navegador.page_source
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')

    pokedex_numeros = []
    nombres = []
    for row in rows[1:355]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            pokedex_numero = cols[0].text.strip()
            nombre = cols[1].a.text.strip()
            if pokedex_numero.isdigit():
                pokedex_numeros.append(pokedex_numero)
                nombres.append(nombre)
    df = pd.DataFrame({
         'Numero de Pokedex': pokedex_numeros,
         'Nombre de pokemon': nombres
        })
    print(df)

    navegador.quit()
    df.to_csv('Pokedex.cvs' , index = False)
    return df

def WebscrappingTipos():
    driver = ChromeDriverManager().install()
    service = Service(driver)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get('https://www.wikidex.net/wiki/Tipo')

    time.sleep(7)

    tipos = set()
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    table = soup.find('table', {'class': 'tabpokemon'})
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
               link = cell.find('a')
               if link and 'title' in link.attrs:
                    tipo_nombre = link.attrs['title'].replace("Tipo ", "").strip()
                    if tipo_nombre:
                        tipos.add(tipo_nombre)

    navegador.quit()
    tipos_list = [{'Nombre': tipo} for tipo in sorted(tipos)]
    df = pd.DataFrame(tipos_list)
    df.to_csv('tipos.csv', index=False)
    return df









