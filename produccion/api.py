"""Servicio web para clasificar fotos de perros y gatos.

Arrancarlo:
    uvicorn api:app --host 0.0.0.0 --port 8000

Probarlo:
    curl -F "imagenes=@foto.jpg" http://localhost:8000/clasificar
"""
from typing import List

import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile

from clasificador import Clasificador

MAX_IMAGENES = 32
MAX_BYTES = 10 * 1024 * 1024  # 10 MB por imagen

app = FastAPI(title="Clasificador de perros y gatos", version="1.0")
clasificador = Clasificador()


@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "modelo": clasificador.ruta_modelo,
        "segundos_carga_modelo": round(clasificador.segundos_carga, 3),
        "tensorflow": tf.__version__,
        "gpu": len(tf.config.list_physical_devices("GPU")) > 0,
    }


@app.post("/clasificar")
async def clasificar(imagenes: List[UploadFile] = File(...)):
    if len(imagenes) > MAX_IMAGENES:
        raise HTTPException(400, f"Máximo {MAX_IMAGENES} imágenes por petición")

    contenidos = []
    for imagen in imagenes:
        contenido = await imagen.read()
        if len(contenido) > MAX_BYTES:
            raise HTTPException(413, f"{imagen.filename} pesa más de 10 MB")
        contenidos.append(contenido)

    try:
        resultados = clasificador.clasificar(contenidos)
    except tf.errors.InvalidArgumentError:
        raise HTTPException(400, "Alguno de los archivos no es una imagen válida (JPG, PNG, BMP o GIF)")

    return [{"archivo": i.filename, **r} for i, r in zip(imagenes, resultados)]
