# Clasificador de perros y gatos

Este proyecto pone a prueba los modelos del laboratorio de clasificación de imágenes con redes neuronales convolucionales. Tomé el cuaderno del profesor sin cambiarle la lógica, volví a entrenar los 8 modelos, guardé `modeloCNN_AD`, lo cargué de nuevo y lo usé para clasificar 100 fotos que no están en el dataset (50 perros y 50 gatos de Wikimedia Commons). También medí la precisión, la memoria, el uso del procesador y los tiempos de respuesta.

## Qué hay en el repositorio

| Archivo o carpeta | Contenido |
|---|---|
| `ImageClassification (1).ipynb` | Cuaderno original del profesor |
| `Prueba_Modelo_Perros_Gatos.ipynb` | Mi cuaderno de prueba (sirve en Colab o en Docker) |
| `Prueba_Modelo_Perros_Gatos_ejecutado.ipynb` | El mismo cuaderno ya ejecutado, con todos los resultados y las conclusiones |
| `Informe_Prueba_Modelo_Perros_Gatos.pdf` | Informe final |
| `imagenes_prueba/` | Las 100 fotos de prueba; el autor y la licencia de cada una están en `fuentes.csv` |
| `modelos/` | `modeloCNN_AD` guardado en `.h5` y `.keras` |
| `resultados/` | Tablas (CSV y JSON) y gráficas que salieron del cuaderno |
| `produccion/` | Script, servicio web y Dockerfile para usar el modelo fuera del cuaderno |
| `docker/` | Entorno con TensorFlow 2.20 y GPU para ejecutar el cuaderno |

## Resultado

El modelo guardado acierta el 50 % con las 100 fotos porque responde "gato" en todas. La causa es que en la preparación de las imágenes en escala de grises del cuaderno original se divide dos veces entre 255, y las CNN no alcanzan a aprender con valores tan pequeños. En el cuaderno ejecutado y en el informe está explicado con más detalle.

## Cómo ejecutarlo

En Colab basta con abrir `Prueba_Modelo_Perros_Gatos.ipynb` con GPU y subir `imagenes_prueba.zip` cuando lo pida.

En local, con Docker y una GPU NVIDIA:

```bash
docker build -t tf-lab:2.20 docker/
bash docker/ejecutar_cuaderno.sh "Prueba_Modelo_Perros_Gatos.ipynb" "Prueba_Modelo_Perros_Gatos_ejecutado.ipynb"
```

Para usar el modelo como servicio, ver [produccion/README.md](produccion/README.md).

Las fotos de `imagenes_prueba/` son de Wikimedia Commons y conservan sus licencias originales (la mayoría CC BY-SA).
