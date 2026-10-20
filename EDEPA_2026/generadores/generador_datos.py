"""Genera bases numéricas para las preguntas de medidas estadísticas."""
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd


def generar_base_sintetica(n: int = 100, seed: int = 123) -> pd.DataFrame:
    """Crea columnas numéricas válidas para calcular medidas estadísticas."""
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "Edad": np.round(rng.uniform(18, 80, size=n), 1),
            "Visitas": rng.integers(0, 11, size=n),
            "Peso": np.round(rng.normal(70, 15, size=n), 1),
            "Estatura": np.round(rng.normal(1.68, 0.10, size=n), 2),
        }
    )


def asegurar_bases_hermanas(
    out_dir: Path, hermanas: List[Tuple[str, int]], n: int = 100
) -> List[str]:
    """Crea las bases hermanas que aún no existan y retorna sus rutas."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rutas = []

    for sufijo, seed in hermanas:
        ruta = out_dir / f"base_hermana_{sufijo}.xlsx"
        if not ruta.exists():
            generar_base_sintetica(n=n, seed=seed).to_excel(
                ruta, index=False, sheet_name="Datos"
            )
            print(f"Generada base: {ruta}")
        else:
            print(f"Base existente: {ruta}")
        rutas.append(str(ruta))

    return rutas
