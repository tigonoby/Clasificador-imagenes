# Imagen para correr el clasificador como servicio web (solo CPU).
# Se construye desde la carpeta principal del proyecto:
#   docker build -f produccion/Dockerfile -t clasificador-perros-gatos .
FROM python:3.12-slim

WORKDIR /app

COPY produccion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY modelos/perros-gatos-cnn-ad.keras /app/modelos/perros-gatos-cnn-ad.keras
COPY produccion/clasificador.py produccion/clasificar.py produccion/api.py /app/

ENV RUTA_MODELO=/app/modelos/perros-gatos-cnn-ad.keras \
    TF_CPP_MIN_LOG_LEVEL=2 \
    CUDA_VISIBLE_DEVICES=-1

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
