# Movie Data API

## Descripción

Esta API ha sido desarrollada utilizando FastAPI para disponibilizar datos de películas. La API permite realizar consultas sobre películas, actores, y directores usando un dataset público almacenado en Google Drive. El proyecto está diseñado para ser desplegado en Render.

## Características

La API incluye los siguientes endpoints:

1. **Cantidad de filmaciones por mes**
   - `GET /cantidad_filmaciones_mes/{mes}`
   - Devuelve la cantidad de películas estrenadas en el mes consultado.

2. **Cantidad de filmaciones por día**
   - `GET /cantidad_filmaciones_dia/{dia}`
   - Devuelve la cantidad de películas estrenadas en el día de la semana consultado.

3. **Score de una filmación**
   - `GET /score_titulo/{titulo}`
   - Devuelve el título, año de estreno, y score de la película.

4. **Votos de una filmación**
   - `GET /votos_titulo/{titulo}`
   - Devuelve el título, cantidad de votos y promedio de las votaciones de la película.

5. **Información sobre un actor**
   - `GET /get_actor/{nombre_actor}`
   - Devuelve el éxito del actor medido por retorno de inversión, la cantidad de películas en las que ha participado y el promedio de retorno.

6. **Información sobre un director**
   - `GET /get_director/{nombre_director}`
   - Devuelve el éxito del director medido por retorno de inversión, así como detalles de cada película dirigida.

## Requisitos

- Python 3.7+
- FastAPI
- Uvicorn
- Pandas
- Requests

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

Esta API utiliza datos almacenados en Google Drive. Asegúrate de que los archivos `.csv` estén disponibles públicamente y que tengas los IDs correctos para descargarlos.

Modifica el archivo `API.py` si es necesario para actualizar los IDs de los archivos de Google Drive:

```python
movies_df = download_public_gdrive_file('ID_DEL_PRIMER_ARCHIVO')
credits_df = download_public_gdrive_file('ID_DEL_SEGUNDO_ARCHIVO')
