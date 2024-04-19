import json
import matplotlib.pyplot as plt
import pandas as pd

# Charger les données JSON
with open('data.json', 'r', encoding='utf-8') as f:
    jeux_data = json.load(f)

# Convertir les données en DataFrame pandas pour une analyse plus facile
df = pd.DataFrame(jeux_data)

# 1. Distribution des jeux par genre
genre_counts = df.explode('Genre')['Genre'].value_counts()
genre_counts.plot(kind='bar', figsize=(12, 6), color='skyblue')
plt.title('Distribution des jeux par genre')
plt.xlabel('Genre')
plt.ylabel('Nombre de jeux')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Distribution des jeux par date de sortie (par année)
df['Release Date'] = pd.to_datetime(df['Release Date'], format='%d/%m/%Y')
release_year_counts = df['Release Date'].dt.year.value_counts().sort_index()
release_year_counts.plot(kind='bar', figsize=(12, 6), color='salmon')
plt.title('Distribution des jeux par année de sortie')
plt.xlabel('Année de sortie du jeux')
plt.ylabel('Nombre de jeux')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 3. Langues supportées par jeu
languages_counts = df.explode('languages')['languages'].value_counts()
languages_counts.plot(kind='bar', figsize=(16, 6), color='lightgreen')
plt.title('Distribution des langues supportées par jeu')
plt.xlabel('Langue')
plt.ylabel('Nombre de jeux')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Espace de stockage requis par jeu (excluant les jeux avec plus de 6000 GB de stockage)
# Nettoyage des données pour obtenir une valeur numérique pour l'espace de stockage
df['Storage:'] = df['Storage:'].str.extract('(\d+)').astype(float)
filtered_df = df[df['Storage:'] < 6000]
filtered_df[['Title', 'Storage:']].dropna().sort_values(by='Storage:', ascending=False).plot(x='Title', y='Storage:', kind='bar', figsize=(16, 6), color='purple')
plt.title('Espace de stockage requis par jeu (excluant > 6000 GB)')
plt.xlabel('Jeu')
plt.ylabel('Espace de stockage requis (GB)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()