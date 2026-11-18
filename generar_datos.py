import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
n = 200
df = pd.DataFrame({
    "id_venta": np.arange(1, n + 1),
    "fecha": pd.date_range("2025-01-01", periods=n).strftime("%Y-%m-%d"),
    "producto": rng.choice(["Cuaderno", "Mochila", "Lapicera", None], n, p=[0.3, 0.3, 0.35, 0.05]),
    "cantidad": rng.integers(1, 8, n),
    "precio_unit": rng.choice([450.0, 1500.0, 18000.0], n),
})
df.to_csv("data/ventas_origen.csv", index=False)
print("Creado data/ventas_origen.csv")
