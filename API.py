from fastapi import FastAPI
import pandas as pd
import ast
import numpy as np
import calendar

app = FastAPI()

# Cargar el dataset
movies_df = pd.read_csv('movies_dataset.csv')
# Aplicar las transformaciones previas
# Aquí incluirías el código que ya usaste para limpiar los datos.
movies_df['revenue'] = movies_df['revenue'].fillna(0)
movies_df['budget'] = movies_df['budget'].fillna(0)
movies_df.dropna(subset=['release_date'], inplace=True)
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
movies_df['release_year'] = movies_df['release_date'].dt.year
movies_df['budget'] = pd.to_numeric(movies_df['budget'], errors='coerce').fillna(0)
movies_df['return'] = movies_df.apply(
    lambda x: x['revenue'] / x['budget'] if x['budget'] > 0 else 0, axis=1
)
columns_to_drop = ['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']
movies_df.drop(columns=columns_to_drop, inplace=True)
collection_df = movies_df['belongs_to_collection'].dropna().apply(eval).apply(pd.Series)
collection_df.columns = ['collection_' + str(col) for col in collection_df.columns]
movies_df = movies_df.join(collection_df)
columns_to_drop = ['collection_0', 'belongs_to_collection']
movies_df.drop(columns=columns_to_drop, inplace=True)
movies_df['genres'] = movies_df['genres'].apply(eval).apply(lambda x: ', '.join([d['name'] for d in x]))
movies_df['production_companies'] = movies_df['production_companies'].apply(
    lambda x: ', '.join([d['name'] for d in ast.literal_eval(x)]) if isinstance(x, str) and x.startswith('[') else ''
)
movies_df['production_countries'] = movies_df['production_countries'].apply(
    lambda x: ', '.join([d['name'] for d in ast.literal_eval(x)]) if isinstance(x, str) and x.startswith('[') else np.nan
)
movies_df['spoken_languages'] = movies_df['spoken_languages'].apply(
    lambda x: ', '.join([d['name'] for d in ast.literal_eval(x)]) if isinstance(x, str) and x.startswith('[') else np.nan
)
# Definir las funciones para cada endpoint
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    # Diccionario para convertir el mes en español a número
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    mes = mes.lower()  # Convertir el mes a minúsculas para evitar errores de entrada
    if mes in meses:
        month_number = meses[mes]
        count = movies_df[movies_df['release_date'].dt.month == month_number].shape[0]
        return {"mensaje": f"{count} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}
    else:
        return {"mensaje": "Mes no válido. Por favor ingrese un mes en español."}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    # Convertir el día a número (0 = lunes, 6 = domingo)
    day_number = list(calendar.day_name).index(dia.capitalize())
    count = movies_df[movies_df['release_date'].dt.dayofweek == day_number].shape[0]
    return {"mensaje": f"{count} cantidad de películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        año = pelicula['release_year'].values[0]
        score = pelicula['popularity'].values[0]  # Asegúrate que este sea el campo correcto
        return {"mensaje": f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}"}
    else:
        return {"mensaje": f"La película {titulo} no fue encontrada."}

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        votos = pelicula['vote_count'].values[0]
        promedio = pelicula['vote_average'].values[0]
        if votos >= 2000:
            return {"mensaje": f"La película {titulo} fue estrenada en el año {pelicula['release_year'].values[0]}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"}
        else:
            return {"mensaje": f"La película {titulo} no cumple con la condición de tener al menos 2000 valoraciones."}
    else:
        return {"mensaje": f"La película {titulo} no fue encontrada."}

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    credits_df = pd.read_csv('credits.csv')  # Cargar el archivo de créditos
    actor_films = credits_df[credits_df['cast'].str.contains(nombre_actor, case=False, na=False)]
    
    if not actor_films.empty:
        film_count = actor_films.shape[0]
        total_return = movies_df[movies_df['id'].isin(actor_films['id'])]['return'].sum()
        avg_return = total_return / film_count
        return {"mensaje": f"El actor {nombre_actor} ha participado de {film_count} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {avg_return} por filmación"}
    else:
        return {"mensaje": f"El actor {nombre_actor} no fue encontrado en el dataset."}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    credits_df = pd.read_csv('credits.csv')  # Cargar el archivo de créditos
    director_films = credits_df[credits_df['crew'].str.contains(nombre_director, case=False, na=False)]
    
    if not director_films.empty:
        director_films = director_films[director_films['job'] == 'Director']
        films = movies_df[movies_df['id'].isin(director_films['id'])]
        details = films[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')
        return {"mensaje": details}
    else:
        return {"mensaje": f"El director {nombre_director} no fue encontrado en el dataset."}
