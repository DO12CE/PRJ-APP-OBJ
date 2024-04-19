import requests
from bs4 import BeautifulSoup
from datetime import datetime

links = []
url = 'https://store.steampowered.com/app/730/CounterStrike_2/'
response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trouver toutes les balises <a> contenant des liens
    for a_tag in soup.find_all('a', href=True):
        # Extraire l'URL
        link = a_tag['href']
        # Vérifier si l'URL est complète et valide
        if link.startswith('https://store.steampowered.com/app/'):
            links.append(link)

tab=[]

for link in links:
    url = link
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver la balise div avec l'ID 'genresAndManufacturer'
    genres_and_manufacturer_div = soup.find('div', {'id': 'genresAndManufacturer'})
    game_area_div = soup.find('div', {'class': 'game_area_sys_req sysreq_content active'})

    dictionnaire = {}

    # Extraire les données de la balise
    if genres_and_manufacturer_div:
        data = genres_and_manufacturer_div.text.strip()
    
        # Séparer les différentes lignes de données
        lignes = data.split('\n')
    
        for ligne in lignes:
            # Séparer la clé et la valeur
            if ': ' in ligne:
                cle, valeur = ligne.split(': ', 1)
                dictionnaire[cle] = valeur
    
        if 'Genre' in dictionnaire and ',' in dictionnaire['Genre']:
            # Diviser la valeur en une liste en supprimant la virgule et l'espace
            genres = dictionnaire['Genre'].split(', ')
    
        # Mettre à jour la valeur de la clé 'Genre' dans le dictionnaire
        dictionnaire['Genre'] = genres
        
        # Convertir la chaîne de caractères en date
        if 'Release Date' in dictionnaire:
            date_str = dictionnaire['Release Date']
            date_obj = datetime.strptime(date_str, '%d %b, %Y').date()

            # Convertir la date au format 'dd/mm/yyyy' avec des slashes
            date_formatee = date_obj.strftime('%d/%m/%Y')

            # Mettre à jour le dictionnaire avec la date au format date
            dictionnaire['Release Date'] = date_formatee
        
        
    else:
        print("Balise non trouvée")
    


    # Extraire les données de la balise
    if game_area_div:
        data = game_area_div.find_all('ul')
    
        # Rechercher la balise ul contenant les spécifications minimales
        for ul in data:
            strong_tag = ul.find('strong')
        
            if strong_tag and strong_tag.text == 'Minimum:':
                li_tags = ul.find_all('li')
            
                for li in li_tags:
                    strong_tag = li.find('strong')
                
                    # Vérifier si strong_tag est différent de None avant d'accéder à son attribut text
                    if strong_tag:
                        cle = strong_tag.text.replace('\xa0', ' ')
                        valeur = li.text.split(': ')[1].replace('\xa0', ' ')
                        dictionnaire[cle] = valeur
    else:
        print("Balise non trouvée")
    
    
    # Trouver la balise strong pour les recommandations Minimales
    strong_tag = soup.find('strong', text='Minimale')

    if strong_tag:
        ul_tag = strong_tag.find_next('ul', class_='bb_ul')
    
        if ul_tag:
            li_tags = ul_tag.find_all('li')
        
            for li in li_tags:
                # Séparer la clé et la valeur à partir du texte du <li>
                parts = li.text.split(': ')
            
                # Vérifier si la séparation a réussi et ajouter au dictionnaire
                if len(parts) == 2:
                    cle = parts[0].replace('\xa0', ' ')
                    valeur = parts[1].replace('\xa0', ' ')
                    dictionnaire[cle] = valeur

            

    # Extraire les langues disponibles
    langues = []
    table_langues = soup.find('table', {'class': 'game_language_options'})
    if table_langues:
        rows = table_langues.find_all('tr')
        for row in rows[1:]:  # Omettre la première ligne qui contient les en-têtes
            langue = row.find('td', {'class': 'ellipsis'}).text.strip()
            langues.append(langue)

    dictionnaire['languages'] = langues


    tab.append(dictionnaire)
    #print(dictionnaire)
    
print(tab)        
    