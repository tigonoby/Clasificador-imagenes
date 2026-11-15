#!/usr/bin/env bash
# Ejecuta un cuaderno Jupyter sin interfaz (papermill) dentro de tf-lab:2.20 con GPU.
# Uso (desde Git Bash, en cualquier carpeta):
#   bash "docker/ejecutar_cuaderno.sh" "ImageClassification (1).ipynb" "salida.ipynb"
# Las rutas de entrada/salida son relativas a la carpeta del proyecto (/tf/proyecto).
# El dataset de TFDS se cachea en el volumen Docker "tfds-cache".
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "Uso: $0 <cuaderno_entrada.ipynb> <cuaderno_salida.ipynb>" >&2
  exit 1
fi
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROYECTO="$(cd "$DIR" && (pwd -W 2>/dev/null || pwd))"
export MSYS_NO_PATHCONV=1
docker run --rm --gpus all --shm-size=2g \
  -v "${PROYECTO}":/tf/proyecto \
  -v tfds-cache:/root/tensorflow_datasets \
  -w /tf/proyecto \
  tf-lab:2.20 \
  papermill "$1" "$2" --log-output --kernel python3
