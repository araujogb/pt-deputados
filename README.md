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
deputados fetch
deputados --help
```

---

## 📊 Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| bid | int64 | Unique deputy ID |
| full_name | string | Full legal name |
| short_name | string | Common/public name |
| party | string | Political party |
| circle | string | Electoral circle |
| email | string | Parliamentary email |
| scraped_at | datetime | When scraped |

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
