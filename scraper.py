import asyncio
import httpx
from pathlib import Path
import polars as pl
from tqdm.asyncio import tqdm
from datetime import date

from parsers import parse_deputy_list, parse_biography


async def fetch(url: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore) -> str:
    """Polite async HTTP get"""
    async with semaphore:
        resp = await client.get(
            url,
            headers={
                "User-Agent": "PTDeputadosScraper/1.0 (+https://github.com/araujogb/pt-deputados)"
            }
        )
        resp.raise_for_status()
        await asyncio.sleep(0.25)   # Be nice to the parliament servers
        return resp.text


async def main():
    """Full scrape: list page + all 230 biography pages"""
    Path("raw/bios").mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(exist_ok=True)

    async with httpx.AsyncClient(timeout=40.0, limits=httpx.Limits(max_connections=6)) as client:
        sem = asyncio.Semaphore(5)

        print("🔍 1/3 Scraping the main deputy list...")
        list_html = await fetch(
            "https://www.parlamento.pt/DeputadoGP/paginas/deputadoslista.aspx",
            client, sem
        )
        base_deputies = parse_deputy_list(list_html)
        print(f"✅ Found {len(base_deputies)} deputies")

        print("📄 2/3 Downloading all biography pages (this takes ~2 minutes)...")
        tasks = [fetch(dep["bio_url"], client, sem) for dep in base_deputies]
        bio_htmls = await tqdm.gather(*tasks, desc="Downloading biographies")

        print("🔬 3/3 Parsing and structuring data...")
        deputies_data = []
        for base, html in zip(base_deputies, bio_htmls):
            try:
                deputy = parse_biography(html, base)
                deputies_data.append(deputy.model_dump(mode="json"))

                # Save raw HTML (useful for debugging or re-parsing later)
                Path(f"raw/bios/{base['bid']}.html").write_text(html, encoding="utf-8")
            except Exception as e:
                print(f"⚠️  Parsing error for BID {base['bid']}: {e}")

        # Save the final clean datasets
        df = pl.DataFrame(deputies_data)
        df.write_parquet("data/deputies.parquet", compression="zstd")
        df.write_ndjson("data/deputies.jsonl")

        print(f"\n🎉 SUCCESS! {len(deputies_data)} deputies fully scraped and saved.")
        print("   📊 Best file: data/deputies.parquet   (use in Python or R)")
        print("   📄 Also saved: data/deputies.jsonl")
        print(f"   📅 Date: {date.today().isoformat()}")


if __name__ == "__main__":
    asyncio.run(main())
