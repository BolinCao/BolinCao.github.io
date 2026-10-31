from datetime import datetime, timezone
from html import unescape
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = Path(__file__).resolve().parent / "results"
HOMEPAGE = REPO_ROOT / "_pages" / "about.md"
USER_AGENT = "BolinCaoAcademicPage/1.0 (mailto:bolincao@foxmail.com)"

# Used only when Crossref is temporarily unavailable. These values seed the
# first successful workflow run and prevent a transient API outage from
# breaking the website or the scheduled GitHub Action.
FALLBACK_COUNTS = {
    "10.1249/mss.0000000000003961": 0,
    "10.1002/dad2.70303": 0,
    "10.1093/braincomms/fcaf083": 7,
    "10.1016/j.psychsport.2024.102678": 7,
    "10.1093/braincomms/fcad069": 12,
    "10.1016/j.nicl.2021.102797": 10,
    "10.1016/j.nicl.2019.102071": 60,
}


def homepage_publications():
    text = HOMEPAGE.read_text(encoding="utf-8")
    publications = []
    for article in re.findall(
        r'<article class="publication-item">(.*?)</article>', text, flags=re.DOTALL
    ):
        title_match = re.search(r"<h3>(.*?)</h3>", article, flags=re.DOTALL)
        doi_match = re.search(r'href="https://doi\.org/([^"?#]+)', article)
        if title_match and doi_match:
            title = unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
            publications.append({"title": title, "doi": doi_match.group(1).strip()})
    if not publications:
        raise RuntimeError(f"No DOI-tagged publications found in {HOMEPAGE}")
    return publications


def crossref_citation_count(doi, attempts=4):
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=30) as response:
                record = json.load(response)["message"]
            return int(record.get("is-referenced-by-count", 0))
        except (HTTPError, URLError, TimeoutError, KeyError, TypeError, ValueError) as error:
            if attempt == attempts - 1:
                print(f"Crossref lookup failed for {doi}: {error}")
                return None
            time.sleep(2 ** attempt)


def build_citation_data():
    records = {}
    fallback_dois = []
    for publication in homepage_publications():
        doi = publication["doi"]
        count = crossref_citation_count(doi)
        if count is None:
            fallback_dois.append(doi)
            count = FALLBACK_COUNTS.get(doi.lower(), 0)
        records[doi] = {
            "author_pub_id": doi,
            "bib": {"title": publication["title"]},
            "num_citations": count,
            "doi": doi,
        }

    return {
        "name": "Bolin Cao",
        "source": "Crossref",
        "updated": datetime.now(timezone.utc).isoformat(),
        "citedby": sum(record["num_citations"] for record in records.values()),
        "publications": records,
        "fallback_dois": fallback_dois,
    }


def main():
    citation_data = build_citation_data()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with (RESULTS_DIR / "gs_data.json").open("w", encoding="utf-8") as outfile:
        json.dump(citation_data, outfile, ensure_ascii=False, indent=2)

    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(citation_data["citedby"]),
    }
    with (RESULTS_DIR / "gs_data_shieldsio.json").open(
        "w", encoding="utf-8"
    ) as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)

    print(json.dumps(citation_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
