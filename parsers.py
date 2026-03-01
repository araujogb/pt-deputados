from bs4 import BeautifulSoup
import re
from datetime import datetime
from models import Deputy, Commission

def parse_deputy_list(html: str) -> list[dict]:
    """FINAL robust parser - exact match to live HTML + deduplication"""
    soup = BeautifulSoup(html, "html.parser")
    deputies_dict = {}   # BID → data (prevents duplicates)

    for row in soup.find_all("div", class_=re.compile(r"row.*margin_h0.*margin-Top-15")):
        cols = row.find_all("div", class_="col-xs-12")
        if len(cols) < 3:
            continue

        # Name column
        name_col = cols[0]
        a = name_col.find("a", href=re.compile(r"Biografia\.aspx\?BID=\d+"))
        if not a:
            continue
        bid = int(re.search(r"BID=(\d+)", a["href"]).group(1))
        short_name = a.get_text(strip=True)

        # Circle column (2nd col)
        circle = "Desconhecido"
        if "Círculo Eleitoral" in cols[1].get_text():
            span = cols[1].find("span", class_="TextoRegular")
            if span:
                circle = span.get_text(strip=True)

        # Party column (3rd col)
        party = "Independente"
        if any(x in cols[2].get_text() for x in ["Grupo Parlamentar", "Partido"]):
            span = cols[2].find("span", class_="TextoRegular")
            if span:
                party = span.get_text(strip=True)

        # Store (last occurrence wins - fixes the first-row duplicate)
        deputies_dict[bid] = {
            "bid": bid,
            "short_name": short_name,
            "circle": circle,
            "party": party,
            "bio_url": f"https://www.parlamento.pt/DeputadoGP/Paginas/Biografia.aspx?BID={bid}"
        }

    return list(deputies_dict.values())


def parse_biography(html: str, base_data: dict) -> Deputy:
    """Bio parser (already perfect)"""
    soup = BeautifulSoup(html, "html.parser")
    data = base_data.copy()
    
    text_nodes = [t.strip() for t in soup.find_all(string=True) if t.strip()]
    i = 0
    while i < len(text_nodes):
        label = text_nodes[i]
        if i + 1 < len(text_nodes):
            value = text_nodes[i + 1]
            if "Nome completo" in label:
                data["full_name"] = value
            elif "Data de nascimento" in label:
                for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
                    try:
                        data["birth_date"] = datetime.strptime(value.strip(), fmt).date()
                        break
                    except:
                        pass
            elif any(x in label for x in ["Habilitações literárias", "Habilitações"]):
                data["education"] = [line.strip() for line in value.splitlines() if line.strip()]
            elif "Profissão" in label:
                data["profession"] = value
            elif any(x in label for x in ["Cargos exercidos", "Cargos anteriormente"]):
                data["previous_cargos"] = [line.strip() for line in value.splitlines() if line.strip()]
            elif "Comissões Parlamentares" in label:
                commissions = []
                for line in value.splitlines():
                    line = line.strip()
                    if line:
                        if "[" in line and "]" in line:
                            name, role = line.split("[", 1)
                            commissions.append(Commission(name=name.strip(), role=role.strip("]")))
                        else:
                            commissions.append(Commission(name=line))
                data["current_commissions"] = commissions
        i += 1
    
    # Photo
    img = soup.find("img", alt=re.compile("foto|deputado", re.I)) or soup.find("img", class_=re.compile("foto|deputado", re.I))
    if img and img.get("src"):
        src = img["src"]
        if src.startswith("/"):
            src = "https://www.parlamento.pt" + src
        data["photo_url"] = src
    
    return Deputy(**data)
