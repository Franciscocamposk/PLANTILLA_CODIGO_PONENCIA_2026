# EDEPA 2026 — Generador de evaluaciones de medidas estadísticas

Sistema automatizado para generar **versiones paralelas** de una evaluación sobre medidas de resumen (media, mediana, cuartiles y deciles). Produce enunciados LaTeX/PDF, soluciones comentadas y bases de datos Excel listas para el estudiante.

Diseñado para contextos académicos (laboratorios, exámenes y materiales de ponencia) donde se requieren variantes equivalentes con datos distintos.

---

## Características

- Generación de **3 versiones** (V1, V2, V3) a partir de bases «hermanas» sintéticas
- Preguntas aleatorias sobre **medidas estadísticas** de una variable numérica
- Salida en **LaTeX** (`.tex`) y, si hay `pdflatex`, compilación automática a **PDF**
- Documento de **solución** con procedimiento e interpretación
- Bases Excel (`base_hermana_A.xlsx`, `B`, `C`) con variables: Edad, Visitas, Peso, Estatura
- Semillas fijas para resultados **reproducibles**

---

## Estructura del proyecto

```text
PLANTILLA_CODIGO_PONENCIA_2026/
├── README.md
└── EDEPA_2026/
    ├── Pregunta_EDEPA.py          # Script principal
    ├── requirements.txt           # Dependencias Python
    ├── generadores/
    │   ├── generador_datos.py     # Bases sintéticas Excel
    │   ├── generador_preguntas.py # Formulación de la pregunta y solución
    │   ├── generador_latex.py     # Plantillas y documentos .tex
    │   └── compilador_latex.py    # Compilación con pdflatex
    ├── EDEPA_Version_1/
    │   ├── Datos/                 # base_hermana_A.xlsx
    │   ├── Enunciado/             # EDEPA_V1.tex / .pdf
    │   └── Solucion/              # EDEPA_V1_SOL.tex / .pdf
    ├── EDEPA_Version_2/
    └── EDEPA_Version_3/
```

---

## Requisitos

| Componente | Detalle |
|------------|---------|
| Python | 3.10 o superior (recomendado) |
| Dependencias | `numpy`, `pandas`, `openpyxl` |
| LaTeX (opcional) | Distribución con `pdflatex` (TeX Live, MiKTeX, etc.) |

Sin LaTeX instalado, el programa genera únicamente los archivos `.tex`.

---

## Instalación

```bash
cd EDEPA_2026
python -m pip install -r requirements.txt
```

---

## Uso

Desde el directorio `EDEPA_2026`:

```bash
python Pregunta_EDEPA.py
```

El script:

1. Crea (o reutiliza) tres bases Excel hermanas con 100 filas cada una  
2. Selecciona una variable numérica y formula una pregunta de medidas estadísticas  
3. Escribe enunciado y solución en LaTeX por versión  
4. Compila a PDF si `pdflatex` está disponible  

### Salida esperada (por versión)

| Carpeta | Contenido |
|---------|-----------|
| `Datos/` | Archivo Excel de la base correspondiente |
| `Enunciado/` | `EDEPA_Vn.tex` y, si aplica, `EDEPA_Vn.pdf` |
| `Solucion/` | `EDEPA_Vn_SOL.tex` y, si aplica, `EDEPA_Vn_SOL.pdf` |

---

## Módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| `Pregunta_EDEPA.py` | Orquestación: bases → preguntas → LaTeX → PDF |
| `generador_datos.py` | Generación de bases sintéticas reproducibles |
| `generador_preguntas.py` | Enunciado, cálculo e interpretación de medidas |
| `generador_latex.py` | Ensamblado del documento con encabezado de curso |
| `compilador_latex.py` | Verificación de `pdflatex` y compilación limpia |

---

## Personalización

- **Metadatos del documento** (código de curso, laboratorio, fecha, duración): editar `CURSO_INFO` en `generadores/generador_latex.py`
- **Número de filas / semillas de las bases**: ajustar `N_FILAS` y `HERMANAS` en `Pregunta_EDEPA.py`
- **Plantilla LaTeX**: si existe `recursos/plantillas/plantilla_laboratorio.tex` en el directorio padre, se usa; si no, se aplica una plantilla mínima integrada

---

## Notas

- Las versiones comparten el mismo tipo de ítem, pero usan datos y variables distintos para reducir copia entre grupos.
- Los valores numéricos en la solución se presentan con **dos decimales** y coma decimal (formato local).
- Los archivos auxiliares de LaTeX se eliminan tras una compilación exitosa (`clean=True`).

---

## Licencia y uso académico

Material orientado a fines educativos y de ponencia. Adapte metadatos, plantillas y contenidos según las normas de su institución.
