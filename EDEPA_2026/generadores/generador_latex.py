"""Genera los documentos LaTeX de la pregunta y su solución."""
from pathlib import Path


CURSO_INFO = {
    "codigo": "MAT003",
    "nombre": "Cálculo II",
    "laboratorio": "Laboratorio 1",
    "ciclo": "II Ciclo 2025",
    "facultad": "Facultad de Ciencias Exactas y Naturales",
    "fecha": "Lunes  1 de setiembre de 2025",
    "duracion": "2 horas",
}


def tex_escape(texto):
    """Escapa caracteres especiales de LaTeX en texto generado."""
    reemplazos = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(reemplazos.get(caracter, caracter) for caracter in str(texto))


def _cargar_plantilla(plantilla_path):
    ruta = Path(plantilla_path)
    if ruta.exists():
        return ruta.read_text(encoding="utf-8") + "\n"

    return (
        r"\documentclass[12pt]{article}" + "\n"
        r"\usepackage[utf8]{inputenc}" + "\n"
        r"\usepackage{graphicx}" + "\n"
        r"\usepackage{enumerate}" + "\n"
        r"\newcommand{\pt}[1]{\textbf{(#1 pts)}}" + "\n"
    )


def _generar_encabezado(version_num, total_pts, es_solucion=False):
    sufijo = " - SOLUCIONES" if es_solucion else ""
    fecha = f"{CURSO_INFO['fecha']}\\\\\n" if CURSO_INFO["fecha"] else ""
    return (
        f"\\includegraphics[scale=.25]{{LogoMate.eps}}\n\n"
        f"\\vspace{{-3ex}}\n"
        f"$\\phantom{{x}}$\\hfill {CURSO_INFO['codigo']} "
        f"{CURSO_INFO['nombre']}\\\\\n"
        f"$\\phantom{{x}}$\\hfill {CURSO_INFO['laboratorio']}, "
        f"{CURSO_INFO['ciclo']}\\\\[1ex]\n"
        f"{CURSO_INFO['facultad']}\\hfill Duración: "
        f"{CURSO_INFO['duracion']}\\\\\n"
        f"{fecha}"
        f"Puntaje total: {total_pts} puntos\n"
        f"\\vspace{{-1ex}}\n\\hrulefill\n"
        f"\\hfill v{version_num}{sufijo}\n\n"
    )


def _total_puntos(items):
    return int(sum(item[-1] for item in items))


def generar_tex_evaluacion(items, version_num, out_path, plantilla_path):
    preambulo = _cargar_plantilla(plantilla_path)
    cuerpo = "\\begin{enumerate}\n"
    for _, enunciado, _, _, _, puntos in items:
        cuerpo += f"  \\item \\pt{{{puntos}}} {enunciado}\n"
    cuerpo += "\\end{enumerate}\n"

    contenido = (
        preambulo
        + r"\begin{document}"
        + "\n"
        + _generar_encabezado(version_num, _total_puntos(items))
        + cuerpo
        + r"\end{document}"
    )
    Path(out_path).write_text(contenido, encoding="utf-8")
    print(f"Generada evaluación: {out_path}")


def generar_tex_soluciones(items, version_num, out_path, plantilla_path):
    preambulo = _cargar_plantilla(plantilla_path)
    cuerpo = ""
    for numero, (_, enunciado, solucion_texto, solucion_detalle, _, puntos) in enumerate(
        items, start=1
    ):
        cuerpo += (
            f"\\section*{{Pregunta {numero} \\pt{{{puntos}}}}}\n"
            f"{enunciado}\n\n"
            f"\\paragraph{{Solución y retroalimentación:}} "
            f"{tex_escape(solucion_detalle or solucion_texto)}\n"
        )

    contenido = (
        preambulo
        + r"\begin{document}"
        + "\n"
        + _generar_encabezado(
            version_num, _total_puntos(items), es_solucion=True
        )
        + cuerpo
        + r"\end{document}"
    )
    Path(out_path).write_text(contenido, encoding="utf-8")
    print(f"Generadas soluciones: {out_path}")
