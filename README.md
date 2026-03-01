# 🏛️ Deputados da Assembleia da República (XVII Legislatura)

Scraper moderno + dados limpos de todos os **230 deputados** da Assembleia da República Portuguesa.

**Última atualização:** Auto-updated monthly via GitHub Actions

---

## 📦 Instalação

See installation instructions in the repository.

---

## 🚀 Usage

deputados fetch
deputados --help

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

## 📈 Current Data

230 deputies from 8 parties (PSD, CH, PS, IL, L, PCP, CDS-PP, Others)

---

## 💻 Examples

See examples/python_usage.py and examples/r_usage.R

---

## 📝 License

CC0-1.0 (Public Domain)

Data sourced from Assembleia da República.