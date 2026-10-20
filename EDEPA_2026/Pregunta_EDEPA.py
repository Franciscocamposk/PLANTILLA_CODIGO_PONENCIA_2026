"""
Genera versiones de EDEPA_2026 con una pregunta de medidas estadísticas.

Uso:
    python -m pip install -r requirements.txt
    python Pregunta_EDEPA.py
"""
from pathlib import Path
import shutil
import tempfile

try:
    import numpy as np
    import pandas as pd
except ModuleNotFoundError as error:
    if error.name in {"numpy", "pandas"}:
        raise SystemExit(
            "Falta una dependencia de EDEPA_2026. Instálala en el mismo "
            "intérprete con el que ejecutas este script: "
            "python -m pip install -r requirements.txt"
        ) from error
    raise

from generadores.compilador_latex import compilar_latex, verificar_latex_instalado
from generadores.generador_datos import asegurar_bases_hermanas
from generadores.generador_latex import generar_tex_evaluacion, generar_tex_soluciones
from generadores.generador_preguntas import is_num, q_random_summary_stats


SCRIPT_DIR = Path(__file__).parent.resolve()
HERMANAS = [("A", 100), ("B", 101), ("C", 102)]
N_FILAS = 100
SEED_BASE = 20250831
ROOT_OUT = SCRIPT_DIR
RECURSOS_DIR = SCRIPT_DIR.parent / "recursos"
PLANTILLA_PATH = RECURSOS_DIR / "plantillas" / "plantilla_laboratorio.tex"
LOGOS_DIR = RECURSOS_DIR


def generar_evaluacion_por_base(
    df, version_num, plantilla_path, enunciado_dir, solucion_dir
):
    """Genera una evaluación y su solución, cada una con una sola pregunta."""
    columnas_numericas = [col for col in df.columns if is_num(df[col])]
    if not columnas_numericas:
        raise ValueError("La base no contiene variables numéricas para calcular medidas.")

    rng = np.random.default_rng(SEED_BASE + version_num * 100)
    variable = rng.choice(columnas_numericas).item()
    pregunta = ("Q1", *q_random_summary_stats(df, variable, rng=rng, puntos=4))

    logo = LOGOS_DIR / "LogoMate.eps"
    if logo.exists():
        shutil.copy2(logo, enunciado_dir / logo.name)
        shutil.copy2(logo, solucion_dir / logo.name)

    tex_evaluacion = enunciado_dir / f"EDEPA_V{version_num}.tex"
    tex_solucion = solucion_dir / f"EDEPA_V{version_num}_SOL.tex"
    items = [pregunta]

    generar_tex_evaluacion(items, version_num, tex_evaluacion, plantilla_path)
    generar_tex_soluciones(items, version_num, tex_solucion, plantilla_path)
    return tex_evaluacion, tex_solucion


def main():
    """Genera tres versiones de la pregunta y, si es posible, compila sus PDF."""
    compilar = verificar_latex_instalado()
    if not compilar:
        print("pdflatex no está instalado; se generarán únicamente los archivos .tex.")

    with tempfile.TemporaryDirectory() as temp:
        rutas_bases = asegurar_bases_hermanas(
            Path(temp), HERMANAS, N_FILAS
        )
        archivos_tex = []
        ROOT_OUT.mkdir(parents=True, exist_ok=True)

        for version_num, ruta_base in enumerate(rutas_bases, start=1):
            base_path = Path(ruta_base)
            datos = pd.read_excel(base_path, sheet_name=0)

            out_dir = ROOT_OUT / f"EDEPA_Version_{version_num}"
            enunciado_dir = out_dir / "Enunciado"
            solucion_dir = out_dir / "Solucion"
            datos_dir = out_dir / "Datos"
            for directorio in (enunciado_dir, solucion_dir, datos_dir):
                directorio.mkdir(parents=True, exist_ok=True)

            shutil.copy2(base_path, datos_dir / base_path.name)
            archivos_tex.append(
                generar_evaluacion_por_base(
                    datos,
                    version_num,
                    PLANTILLA_PATH,
                    enunciado_dir,
                    solucion_dir,
                )
            )

        print(f"Generadas {len(archivos_tex)} versiones en {ROOT_OUT}")

        if compilar:
            exitos = 0
            fallos = 0
            for tex_evaluacion, tex_solucion in archivos_tex:
                for archivo_tex in (tex_evaluacion, tex_solucion):
                    success, _, message = compilar_latex(archivo_tex, clean=True)
                    if success:
                        exitos += 1
                    else:
                        fallos += 1
                        print(f"Error: {message}")
            print(f"Compilación completada: {exitos} éxitos, {fallos} fallos.")


if __name__ == "__main__":
    main()
