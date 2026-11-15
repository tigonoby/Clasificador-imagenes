"""Clasifica una imagen o todas las imágenes de una carpeta desde la terminal.

Ejemplos:
    python clasificar.py foto.jpg
    python clasificar.py ../imagenes_prueba/perros
    python clasificar.py ../imagenes_prueba --csv resultados.csv
"""
import argparse
import csv
import os
import sys

from clasificador import Clasificador

EXTENSIONES = (".jpg", ".jpeg", ".png", ".bmp", ".gif")


def buscar_imagenes(ruta):
    if os.path.isfile(ruta):
        return [ruta]
    encontradas = []
    for carpeta, _, archivos in os.walk(ruta):
        for nombre in sorted(archivos):
            if nombre.lower().endswith(EXTENSIONES):
                encontradas.append(os.path.join(carpeta, nombre))
    return sorted(encontradas)


def main():
    parser = argparse.ArgumentParser(description="Clasifica fotos de perros y gatos")
    parser.add_argument("ruta", help="Imagen o carpeta con imágenes")
    parser.add_argument("--modelo", help="Ruta del modelo (.keras o .h5)")
    parser.add_argument("--csv", help="Guardar los resultados en este archivo CSV")
    args = parser.parse_args()

    rutas = buscar_imagenes(args.ruta)
    if not rutas:
        sys.exit(f"No encontré imágenes en {args.ruta}")

    clasificador = Clasificador(args.modelo) if args.modelo else Clasificador()
    print(f"Modelo cargado en {clasificador.segundos_carga:.2f} s: {clasificador.ruta_modelo}")

    filas = []
    for ruta in rutas:
        with open(ruta, "rb") as f:
            resultado = clasificador.clasificar([f.read()])[0]
        filas.append({"archivo": ruta, **resultado})
        print(f"{os.path.basename(ruta):30s} {resultado['clase']:6s} "
              f"prob. perro {resultado['probabilidad_perro']:.4f}  "
              f"({resultado['ms_preparar'] + resultado['ms_modelo']:.1f} ms)")

    perros = sum(f["clase"] == "perro" for f in filas)
    print(f"\n{len(filas)} imágenes: {perros} perros y {len(filas) - perros} gatos")

    # Si las imágenes están en carpetas llamadas perros/ y gatos/, también calculo la exactitud
    reales = [("perro" if "perro" in f["archivo"].lower() else
               "gato" if "gato" in f["archivo"].lower() else None) for f in filas]
    if all(reales):
        aciertos = sum(r == f["clase"] for r, f in zip(reales, filas))
        print(f"Exactitud según el nombre de la carpeta: {aciertos}/{len(filas)} "
              f"({aciertos / len(filas):.0%})")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=filas[0].keys())
            escritor.writeheader()
            escritor.writerows(filas)
        print(f"Resultados guardados en {args.csv}")


if __name__ == "__main__":
    main()
