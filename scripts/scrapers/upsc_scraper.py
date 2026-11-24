import ssl
import urllib3
import requests
import hashlib
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LegacySSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_upsc_notices(limit=5):
    """
    Scrapes the latest notifications from Union Public Service Commission (UPSC).
    """
    url = "https://upsc.gov.in/whats-new"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())

    notices = []
    try:
        response = session.get(url, headers=headers, timeout=8)
        if response.status_code != 200:
            return notices

        soup = BeautifulSoup(response.text, "html.parser")
        keywords = ["examination", "recruitment", "advertisement", "final result", "interview", "notification", "civil services", "nda", "cds"]

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"].strip()

            if len(title) > 20 and any(k in title.lower() for k in keywords):
                if href.startswith("/"):
                    full_link = f"https://upsc.gov.in{href}"
                elif href.startswith("http"):
                    full_link = href
                else:
                    full_link = f"https://upsc.gov.in/{href}"

                notice_id = f"upsc_{hashlib.md5(title.encode('utf-8')).hexdigest()[:12]}"

                notices.append({
                    "id": notice_id,
                    "title": title,
                    "department": "Union Public Service Commission (UPSC)",
                    "category": "Central Govt Jobs",
                    "state": "All India",
                    "official_link": "https://upsc.gov.in",
                    "pdf_link": full_link,
                    "source": "UPSC"
                })

                if len(notices) >= limit:
                    break

    except Exception as e:
        print(f"[UPSC] Scraper notice: {e}")

    return notices

if __name__ == "__main__":
    results = get_upsc_notices()
    print(f"Found {len(results)} UPSC notices:")
    for r in results:
        print(f"- {r['title']} -> {r['pdf_link']}")
