"""
Genera la pregunta de medidas estadísticas para una variable numérica.
"""
import numpy as np
import pandas as pd


_PERCENTILES = {
    "Q1": 25,
    "Q2": 50,
    "Q3": 75,
    "D1": 10,
    "D2": 20,
    "D3": 30,
    "D4": 40,
    "D5": 50,
    "D6": 60,
    "D7": 70,
    "D8": 80,
    "D9": 90,
}


def _formatear_numero(valor):
    """Formatea un valor con dos decimales y coma decimal."""
    return f"{valor:.2f}".replace(".", ",")


def _generar_detalle_medida(medida, valor, valores, variable):
    """Redacta el procedimiento y la interpretación de una medida."""
    unidades = {
        "Edad": "años",
        "Visitas": "visitas",
        "Peso": "kg",
        "Estatura": "m",
    }
    unidad = unidades.get(variable, f"unidades de {variable}")
    resultado = _formatear_numero(valor)

    if medida == "media":
        suma = _formatear_numero(valores.sum())
        media = "media aritmética"
        return (
            f"La {media} de la variable {variable} se calcula sumando sus "
            f"{len(valores)} observaciones y dividiendo el resultado entre "
            f"{len(valores)}. La suma es {suma}; por tanto, la media es "
            f"{resultado} {unidad}. Esto representa el promedio de "
            f"{variable.lower()} en las observaciones."
        )

    percentil = 50 if medida == "mediana" else _PERCENTILES[medida]
    if medida == "mediana":
        nombre = "La mediana"
    elif medida.startswith("Q"):
        nombre = f"El cuartil {medida[1:]} ({medida})"
    else:
        nombre = f"El decil {medida[1:]} ({medida})"

    return (
        f"{nombre} de la variable {variable} corresponde al percentil "
        f"{percentil}. Para determinarlo se consideran las {len(valores)} "
        f"observaciones ordenadas de menor a mayor y se obtiene el valor "
        f"asociado con el {percentil} % de la distribución. El resultado es "
        f"{resultado} {unidad}. Esto indica que aproximadamente el "
        f"{percentil} % de las observaciones presentan valores de "
        f"{variable.lower()} menores o iguales a {resultado} {unidad}."
    )


def is_num(series):
    """Indica si la serie tiene tipo numérico."""
    return pd.api.types.is_numeric_dtype(series)


def q_random_summary_stats(df, col, rng=None, puntos=4):
    """Genera una pregunta con dos medidas estadísticas no equivalentes."""
    if rng is None:
        rng = np.random.default_rng()

    valores = pd.to_numeric(df[col], errors="coerce").dropna()
    if valores.empty:
        return f"No hay datos válidos en {col}.", "", "Sin datos.", None, 0

    medidas = {
        "media": lambda x: round(x.mean(), 2),
        "mediana": lambda x: round(np.median(x), 2),
        "Q1": lambda x: round(np.percentile(x, 25), 2),
        "Q2": lambda x: round(np.percentile(x, 50), 2),
        "Q3": lambda x: round(np.percentile(x, 75), 2),
        "D1": lambda x: round(np.percentile(x, 10), 2),
        "D2": lambda x: round(np.percentile(x, 20), 2),
        "D3": lambda x: round(np.percentile(x, 30), 2),
        "D4": lambda x: round(np.percentile(x, 40), 2),
        "D5": lambda x: round(np.percentile(x, 50), 2),
        "D6": lambda x: round(np.percentile(x, 60), 2),
        "D7": lambda x: round(np.percentile(x, 70), 2),
        "D8": lambda x: round(np.percentile(x, 80), 2),
        "D9": lambda x: round(np.percentile(x, 90), 2),
    }

    percentil_50 = {"mediana", "Q2", "D5"}
    pares_validos = [
        (primera, segunda)
        for primera in medidas
        for segunda in medidas
        if primera != segunda
        and not ({primera, segunda} <= percentil_50)
    ]
    seleccion = pares_validos[int(rng.choice(len(pares_validos)))]
    resultados = {medida: medidas[medida](valores) for medida in seleccion}

    enunciado = (
        f"Calcule las siguientes medidas para la variable {col}: "
        f"{' y '.join(seleccion)}."
    )
    solucion = "\n\n".join(
        _generar_detalle_medida(medida, resultado, valores, col)
        for medida, resultado in resultados.items()
    )
    return enunciado, "", solucion, None, puntos
