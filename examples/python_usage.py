"""Example usage of pt-deputados data in Python."""

import polars as pl
from pathlib import Path

data_path = Path("data/deputies.parquet")
df = pl.read_parquet(data_path)

print(f"Total deputies: {len(df)}")
print(f"Parties: {df['party'].n_unique()}")

# Filter by party
psd = df.filter(pl.col("party") == "PSD")
print(f"PSD deputies: {len(psd)}")

# Group by circle
by_circle = df.group_by("circle").len().sort("len", descending=True)
print(by_circle)
