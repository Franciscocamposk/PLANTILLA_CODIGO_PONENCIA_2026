# EDEPA 2026 — Generador de preguntas

Genera **tres versiones paralelas** de una evaluación sobre medidas estadísticas (media, mediana, cuartiles y deciles), con enunciado LaTeX/PDF, solución comentada y base Excel.

Repositorio: [Franciscocamposk/PLANTILLA_CODIGO_PONENCIA_2026](https://github.com/Franciscocamposk/PLANTILLA_CODIGO_PONENCIA_2026)

---

## Requisitos

- Python 3.10+
- Dependencias: `numpy`, `pandas`, `openpyxl`
- Opcional: `pdflatex` (TeX Live / MiKTeX) para compilar PDF

```bash
python -m pip install -r requirements.txt
```

---

## Uso

```bash
python Pregunta_EDEPA.py
```

El script:

1. Crea tres bases hermanas (A, B, C) con 100 filas  
2. Elige una variable numérica y formula una pregunta de dos medidas  
3. Genera enunciado y solución en `.tex`  
4. Compila a PDF si `pdflatex` está disponible  

---

## Salida

| Carpeta | Contenido |
|---------|-----------|
| `EDEPA_Version_n/Datos/` | `base_hermana_*.xlsx` |
| `EDEPA_Version_n/Enunciado/` | `EDEPA_Vn.tex` / `.pdf` |
| `EDEPA_Version_n/Solucion/` | `EDEPA_Vn_SOL.tex` / `.pdf` |

---

## Módulos

| Archivo | Función |
|---------|---------|
| `Pregunta_EDEPA.py` | Script principal |
| `generadores/generador_datos.py` | Bases sintéticas |
| `generadores/generador_preguntas.py` | Enunciado y solución |
| `generadores/generador_latex.py` | Documentos `.tex` |
| `compilador_latex.py` | Compilación PDF |

---

## Personalización

- Metadatos del curso: `generadores/generador_latex.py` → `CURSO_INFO`
- Semillas y filas: `Pregunta_EDEPA.py` → `HERMANAS`, `N_FILAS`, `SEED_BASE`
