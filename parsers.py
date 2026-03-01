from bs4 import BeautifulSoup
import re
from datetime import datetime
from models import Deputy, Commission

def parse_deputy_list(html: str) -> list[dict]:
    """Parse deputy list page"""
    soup = BeautifulSoup(html, "html.parser")
    deputies_dict = {}

    for row in soup.find_all("div", class_=re.compile(r"row.*margin_h0.*margin-Top-15")):
        cols = row.find_all("div", class_="col-xs-12")
        if len(cols) < 3:
            continue

        name_col = cols[0]
        a = name_col.find("a", href=re.compile(r"Biografia\.aspx\?BID=\d+"))
        if not a:
            continue
        bid = int(re.search(r"BID=(\d+)", a["href"]).group(1))
        short_name = a.get_text(strip=True)

        circle = "Desconhecido"
        if "Círculo Eleitoral" in cols[1].get_text():
            span = cols[1].find("span", class_="TextoRegular")
            if span:
                circle = span.get_text(strip=True)

        party = "Independente"
        if any(x in cols[2].get_text() for x in ["Grupo Parlamentar", "Partido"]):
            span = cols[2].find("span", class_="TextoRegular")
            if span:
                party = span.get_text(strip=True)

        deputies_dict[bid] = {
            "bid": bid,
            "short_name": short_name,
            "circle": circle,
            "party": party,
            "bio_url": f"https://www.parlamento.pt/DeputadoGP/Paginas/Biografia.aspx?BID={bid}"
        }

    return list(deputies_dict.values())


def _extract_all_field_values(soup: BeautifulSoup, field_keyword: str) -> list[str]:
    """Extract ALL values for a field from ASP.NET repeater controls"""
    values = []
    for span in soup.find_all("span", id=True):
        span_id = span.get("id", "")
        if field_keyword in span_id and "lblText" in span_id:
            text = span.get_text(strip=True)
            if text:
                values.append(text)
    return values


def _extract_single_field(soup: BeautifulSoup, label: str) -> str:
    """Extract single value field"""
    for div in soup.find_all("div", class_="TitulosBio AlinhaL"):
        if label in div.get_text(strip=True):
            value_div = div.find_next_sibling("div")
            if value_div:
                return value_div.get_text(strip=True)
    return ""


def parse_biography(html: str, base_data: dict) -> Deputy:
    """Parse biography page with ALL fields"""
    soup = BeautifulSoup(html, "html.parser")
    data = base_data.copy()
    
    # Single-value fields
    data["full_name"] = _extract_single_field(soup, "Nome completo")
    
    birth_date = _extract_single_field(soup, "Data de nascimento")
    if birth_date:
        for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
            try:
                data["birth_date"] = datetime.strptime(birth_date.strip(), fmt).date()
                break
            except:
                pass
    
    data["profession"] = _extract_single_field(soup, "Profissão")
    
    # Multi-value fields (from ASP.NET repeater controls)
    data["education"] = _extract_all_field_values(soup, "Habilitacoes")
    data["previous_positions"] = _extract_all_field_values(soup, "Cargos")
    
    # Commissions - special handling
    commissions = []
    for span in soup.find_all("span", id=True):
        if "Comissoes" in span.get("id", "") and "lblText" in span.get("id", ""):
            line = span.get_text(strip=True)
            if line:
                if "[" in line and "]" in line:
                    name, role = line.split("[", 1)
                    commissions.append(Commission(name=name.strip(), role=role.strip("]")))
                else:
                    commissions.append(Commission(name=line))
    data["current_commissions"] = commissions
    
    # Photo - extract from background-image style
    photo_url = None
    for div in soup.find_all(style=True):
        style = div.get("style", "")
        if "background-image" in style and "getimage.aspx" in style:
            match = re.search(r'url\(([^)]+)\)', style)
            if match:
                photo_url = match.group(1).strip().strip('"').strip("'")
                break
    data["photo_url"] = photo_url
    
    
    # Add scraped timestamp
    data["scraped_at"] = datetime.now().isoformat()
    
    return Deputy(**data)
