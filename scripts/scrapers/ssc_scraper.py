import ssl
import urllib3
import requests
import hashlib
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ssc_notices(limit=8):
    """
    Scrapes the latest notices and notifications from Staff Selection Commission.
    Uses SSC official regional and central portals for direct PDF links.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    notices = []
    
    # Primary Source: SSC Official Portal via SSCER (direct links to ssc.gov.in PDF attachments)
    try:
        url = "https://www.sscer.org"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            keywords = ["notice", "examination", "cgl", "chsl", "mts", "constable", "recruitment", "schedule", "shortlisted", "admit"]
            skip_words = ["tender", "cleaning", "pest", "vehicle", "car hiring"]

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                href = a["href"].strip()

                if len(title) > 25 and any(k in title.lower() for k in keywords):
                    if any(s in title.lower() for s in skip_words):
                        continue

                    # Resolve full URL
                    if href.startswith("/"):
                        full_link = f"https://www.sscer.org{href}"
                    elif href.startswith("http"):
                        full_link = href
                    else:
                        full_link = f"https://www.sscer.org/{href}"

                    # Clean title from Hindi duplicate if present
                    if "महत्वपूर्ण सूचना" in title or "नोटिस" in title:
                        title_clean = title.split("महत्वपूर्ण")[0].strip()
                        if not title_clean:
                            title_clean = title
                    else:
                        title_clean = title

                    notice_id = f"ssc_{hashlib.md5(title_clean.encode('utf-8')).hexdigest()[:12]}"

                    notices.append({
                        "id": notice_id,
                        "title": title_clean,
                        "department": "Staff Selection Commission (SSC)",
                        "category": "Central Govt Jobs",
                        "state": "All India",
                        "official_link": "https://ssc.gov.in",
                        "apply_link": "https://ssc.gov.in",
                        "pdf_link": full_link,
                        "source": "SSC"
                    })

                    if len(notices) >= limit:
                        break
    except Exception as e:
        print(f"[SSC Scraper] Notice error: {e}")

    return notices

if __name__ == "__main__":
    results = get_ssc_notices()
    print(f"Found {len(results)} SSC notices:")
    for r in results:
        print(f"- {r['title']} -> {r['pdf_link']}")
