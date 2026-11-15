"""Carga el modelo de perros y gatos y clasifica imágenes.

La preparación de cada imagen es la misma que se usó al entrenar en el cuaderno
del profesor. Si se cambia, el modelo recibe datos distintos a los que conoció y
sus respuestas dejan de tener sentido.
"""
import os
import time

import numpy as np
import tensorflow as tf

TAMANO = 100
UMBRAL = 0.5
CLASES = ("gato", "perro")  # 0 = gato, 1 = perro, igual que en cats_vs_dogs
RUTA_MODELO = os.environ.get(
    "RUTA_MODELO",
    os.path.join(os.path.dirname(__file__), "..", "modelos", "perros-gatos-cnn-ad.keras"),
)


def preparar_imagen(contenido):
    """Convierte los bytes de una imagen en el tensor de 100x100x1 que espera el modelo."""
    imagen = tf.io.decode_image(contenido, channels=3, expand_animations=False)  # uint8 RGB

    # Primera preparación del cuaderno (sección 1.3): 100x100 y dividir entre 255
    imagen = tf.image.resize(imagen, (TAMANO, TAMANO))
    imagen = imagen / 255.0

    # Segunda preparación del cuaderno (sección 1.6): gris, 100x100 y otra vez entre 255
    imagen = tf.image.rgb_to_grayscale(imagen)
    imagen = tf.image.resize(imagen, (TAMANO, TAMANO))
    imagen = tf.cast(imagen, tf.float32) / 255.0
    return imagen


class Clasificador:
    def __init__(self, ruta_modelo=RUTA_MODELO):
        inicio = time.perf_counter()
        self.modelo = tf.keras.models.load_model(ruta_modelo, compile=False)
        self.segundos_carga = time.perf_counter() - inicio
        self.ruta_modelo = os.path.abspath(ruta_modelo)
        # La primera llamada siempre es lenta; la hago de una vez al arrancar
        self.modelo(tf.zeros((1, TAMANO, TAMANO, 1)), training=False)

    def clasificar(self, contenidos):
        """Recibe una lista de imágenes en bytes y devuelve un resultado por imagen."""
        inicio = time.perf_counter()
        lote = tf.stack([preparar_imagen(c) for c in contenidos])
        preparado = time.perf_counter()
        probabilidades = self.modelo(lote, training=False).numpy()[:, 0]
        fin = time.perf_counter()

        ms_preparar = (preparado - inicio) * 1000 / len(contenidos)
        ms_modelo = (fin - preparado) * 1000 / len(contenidos)
        resultados = []
        for p in probabilidades:
            clase = CLASES[int(p >= UMBRAL)]
            resultados.append({
                "clase": clase,
                "probabilidad_perro": round(float(p), 6),
                "confianza": round(float(p if clase == "perro" else 1 - p), 6),
                "ms_preparar": round(ms_preparar, 2),
                "ms_modelo": round(ms_modelo, 2),
            })
        return resultados
