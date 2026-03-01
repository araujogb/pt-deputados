# 🏛️ Deputados da Assembleia da República (XVII Legislatura)

Scraper moderno + dados limpos de todos os **230 deputados** da Assembleia da República Portuguesa.

**Última atualização:** Auto-updated monthly via GitHub Actions

---

## 📦 Instalação

```bash
git clone https://github.com/araujogb/pt-deputados.git
cd pt-deputados
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## 🚀 Usage

```bash
# Fetch all deputy data
deputados fetch

# Show help
deputados --help
```

---

## 📊 Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| bid | int | Unique deputy ID |
| short_name | str | Display name |
| full_name | str | Complete legal name |
| birth_date | date | Date of birth |
| circle | str | Electoral circle |
| party | str | Political party |
| education | list | All degrees/certifications |
| profession | str | Current profession |
| previous_positions | list | All previous roles |
| current_commissions | list | Parliamentary commissions |
| bio_url | str | Biography page URL |
| photo_url | str | Photo URL |
| scraped_at | str | ISO timestamp |

---

## 💻 Examples

### Python

```python
import polars as pl

df = pl.read_parquet("data/deputies.parquet")

# Filter by party
psd = df.filter(pl.col("party") == "PSD")

# Count education entries
df.with_columns(
    pl.col("education").list.len().alias("education_count")
)
```

See [examples/python_usage.py](examples/python_usage.py)

### R

```r
library(arrow)
library(dplyr)

df <- read_parquet("data/deputies.parquet")

# Filter by party
psd <- df %>% filter(party == "PSD")
```

See [examples/r_usage.R](examples/r_usage.R)

---

## 📈 Current Data

| Party | Deputies |
|-------|----------|
| PSD | 89 |
| CH | 60 |
| PS | 58 |
| IL | 9 |
| L | 6 |
| PCP | 3 |
| CDS-PP | 2 |
| Others | 3 |
| **Total** | **230** |

---

## 📝 License

**CC0-1.0** (Public Domain) - Free to use for any purpose.

Data sourced from [Assembleia da República](https://www.parlamento.pt).

---

## 🤝 Contributing

Issues and PRs welcome! This is a community project for transparent access to Portuguese parliamentary data.
