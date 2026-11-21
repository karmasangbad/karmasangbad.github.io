import ssl
import urllib3
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LegacySSLAdapter(HTTPAdapter):
    """Adapter to handle legacy TLS renegotiation on Indian government servers."""
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_wbprb_notices(limit=5):
    """
    Scrapes the latest notices from West Bengal Police Recruitment Board (WBPRB).
    """
    url = "https://prb.wb.gov.in"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())

    notices = []
    try:
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[WBPRB] Warning: Received status code {response.status_code}")
            return notices

        soup = BeautifulSoup(response.text, "html.parser")
        keywords = ["recruitment", "constable", "sub-inspector", "police", "warder", "driver", "advt", "notice"]

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"]

            if len(title) > 20 and any(k in title.lower() for k in keywords):
                if href.startswith("/"):
                    full_link = f"https://prb.wb.gov.in{href}"
                elif href.startswith("http"):
                    full_link = href
                else:
                    full_link = f"https://prb.wb.gov.in/{href}"

                notice_id = f"wbprb_{abs(hash(title)) % 1000000}"

                notices.append({
                    "id": notice_id,
                    "title": title,
                    "official_link": "https://prb.wb.gov.in",
                    "pdf_link": full_link,
                    "department": "West Bengal Police Recruitment Board (WBPRB)",
                    "category": "পুলিশ ও ডিফেন্স",
                    "source": "WBPRB"
                })

                if len(notices) >= limit:
                    break

    except Exception as e:
        print(f"[WBPRB] Error scraping: {e}")

    return notices

if __name__ == "__main__":
    results = get_wbprb_notices()
    print(f"Found {len(results)} WBPRB notices:")
    for r in results:
        print(f"- {r['title']} -> {r['pdf_link']}")
