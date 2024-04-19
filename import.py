import json
from url import tab  # Importez le tableau depuis le fichier tableau.py

# Convertir le tableau en JSON
json_data = json.dumps(tab, indent=4, ensure_ascii=False)

# Écrire le JSON dans un fichier
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("Le tableau a été converti et écrit dans data.json.")