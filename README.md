# Prueba del modelo de perros y gatos

Pruebo los modelos del laboratorio *Clasificación de Imágenes con Redes Neuronales Convolucionales*. Sin cambiar el código del profesor: reentreno los 8 modelos, guardo `modeloCNN_AD`, lo cargo y lo uso para clasificar 100 fotos externas (50 perros y 50 gatos de Wikimedia Commons). Mido precisión, memoria, procesamiento y latencias.

## Archivos

| Archivo | Contenido |
|---|---|
| `ImageClassification (1).ipynb` | Cuaderno original del profesor |
| `Prueba_Modelo_Perros_Gatos.ipynb` | Cuaderno nuevo (listo para Colab o Docker) |
| `Prueba_Modelo_Perros_Gatos_ejecutado.ipynb` | El cuaderno nuevo con todas sus salidas |
| `Informe_Prueba_Modelo_Perros_Gatos.pdf` | Informe final |
| `imagenes_prueba/` | Las 100 fotos de prueba; autor y licencia en `fuentes.csv` |
| `modelos/` | `modeloCNN_AD` guardado en `.h5` y `.keras` |
| `resultados/` | Tablas (CSV/JSON) y gráficas |
| `docker/` | Imagen de TensorFlow 2.20 con GPU y script para ejecutar el cuaderno |

## Resultado principal

El modelo guardado acierta el 50 % con las 100 fotos: responde "gato" en todas. La causa es una doble división entre 255 en la preparación de las imágenes en escala de grises del cuaderno original; el informe lo explica.

## Ejecutar

```bash
bash docker/ejecutar_cuaderno.sh "Prueba_Modelo_Perros_Gatos.ipynb" "Prueba_Modelo_Perros_Gatos_ejecutado.ipynb"
```

Las fotos de `imagenes_prueba/` son de Wikimedia Commons y conservan sus licencias originales (en su mayoría CC BY-SA).
