FROM tensorflow/tensorflow:2.20.0-gpu-jupyter

# Paquetes extra para el cuaderno (sin tensorflowjs: podria cambiar la version de TF).
# Se pasa el TF instalado como restriccion para que pip no lo actualice.
# nvidia-cudnn-cu12 9.3: la imagen base trae cuDNN 8, pero TF 2.20 necesita cuDNN 9
# (sin esto TF no registra la GPU). Version = la que fija tensorflow[and-cuda] 2.20.
RUN TFVER=$(python -c "import tensorflow as tf; print(tf.__version__)") && \
    echo "tensorflow==${TFVER}" > /tmp/constraints.txt && \
    pip install --no-cache-dir -c /tmp/constraints.txt \
        tensorflow-datasets psutil scikit-learn pandas matplotlib \
        papermill nbconvert ipykernel pillow seaborn \
        nvidia-cudnn-cu12==9.3.0.75 && \
    python -c "import nvidia.cudnn, os; print(os.path.join(list(nvidia.cudnn.__path__)[0], 'lib'))" > /etc/ld.so.conf.d/000-cudnn9.conf && \
    ldconfig && \
    python -c "import tensorflow as tf; print('TF', tf.__version__)"

# etils (usado por tensorflow-datasets) necesita importlib_resources al preparar datasets
RUN pip install --no-cache-dir -c /tmp/constraints.txt importlib_resources

WORKDIR /tf/proyecto
