# Producción: clasificador de perros y gatos

En esta carpeta está lo necesario para usar el modelo guardado (`modelos/perros-gatos-cnn-ad.keras`) por fuera del cuaderno, ya sea desde la terminal o como servicio web.

| Archivo | Para qué sirve |
|---|---|
| `clasificador.py` | Carga el modelo y prepara cada imagen igual que en el entrenamiento |
| `clasificar.py` | Clasifica una foto o una carpeta completa desde la terminal |
| `api.py` | Servicio web (FastAPI) para clasificar fotos por HTTP |
| `requirements.txt` | Librerías necesarias |
| `Dockerfile` | Imagen lista para desplegar el servicio (solo CPU) |

## Antes de usarlo

El modelo, tal como quedó entrenado en el cuaderno del profesor, responde "gato" a cualquier foto (probabilidad de perro 0,4983 siempre). Esto viene de la doble división entre 255 en la preparación de las imágenes, y está explicado en el cuaderno y en el informe. El código de esta carpeta funciona bien; el problema está en el modelo. Si se entrena un modelo nuevo, basta con cambiar el archivo en `modelos/`, pero hay que ajustar `preparar_imagen()` en `clasificador.py` para que coincida con la preparación que se use en ese entrenamiento.

## Con Docker (recomendado)

Desde la carpeta principal del proyecto:

```bash
docker build -f produccion/Dockerfile -t clasificador-perros-gatos .
docker run -d -p 8000:8000 --name clasificador clasificador-perros-gatos
```

Revisar que esté arriba:

```bash
curl http://127.0.0.1:8000/salud
```

Clasificar una o varias fotos (máximo 32 por petición y 10 MB por foto):

```bash
curl -F "imagenes=@foto1.jpg" -F "imagenes=@foto2.jpg" http://127.0.0.1:8000/clasificar
```

Respuesta:

```json
[{"archivo": "foto1.jpg", "clase": "gato", "probabilidad_perro": 0.498277,
  "confianza": 0.501723, "ms_preparar": 10.74, "ms_modelo": 8.31}]
```

La documentación interactiva del servicio queda en `http://127.0.0.1:8000/docs`.

Para clasificar una carpeta desde la terminal con la misma imagen:

```bash
docker run --rm -v "$(pwd)/imagenes_prueba:/datos" clasificador-perros-gatos python clasificar.py /datos
```

## Sin Docker

Necesita Python 3.9 a 3.12 (TensorFlow 2.20 no funciona con 3.13 o 3.14).

```bash
cd produccion
pip install -r requirements.txt
python clasificar.py ../imagenes_prueba --csv resultados.csv
uvicorn api:app --port 8000
```

## Lo que medí

Probado con las 100 fotos de `imagenes_prueba/`: el modelo carga en unos 0,2 s y cada foto tarda unos 10 ms en prepararse y 8 a 12 ms en clasificarse en CPU. Los resultados son iguales a los del cuaderno (50 % de exactitud, 0 perros y 100 gatos).
