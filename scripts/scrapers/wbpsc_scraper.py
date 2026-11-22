import ssl
import urllib3
import requests
import hashlib
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LegacySSLAdapter(HTTPAdapter):
    """Adapter to handle legacy TLS renegotiation common on Indian government servers."""
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_wbpsc_notices(limit=5):
    """
    Scrapes the latest notices/advertisements from West Bengal Public Service Commission.
    """
    url = "https://psc.wb.gov.in"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())

    notices = []
    try:
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[WBPSC] Warning: Received status code {response.status_code}")
            return notices

        soup = BeautifulSoup(response.text, "html.parser")
        keywords = ["recruitment", "advertisement", "indicative", "scheme", "examination", "interview", "post"]
        
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"].strip()

            if len(title) > 20 and any(k in title.lower() for k in keywords):
                # Clean URL and query parameters
                href_clean = href.replace("&amp;", "&").replace("¶m2", "&param2")
                if href_clean.startswith("Download?"):
                    full_link = f"https://psc.wb.gov.in/{href_clean}"
                elif href_clean.startswith("http"):
                    full_link = href_clean
                else:
                    full_link = f"https://psc.wb.gov.in/{href_clean.lstrip('/')}"

                # Deterministic notice ID
                notice_id = f"wbpsc_{hashlib.md5(title.encode('utf-8')).hexdigest()[:12]}"
                
                notices.append({
                    "id": notice_id,
                    "title": title,
                    "official_link": "https://psc.wb.gov.in",
                    "pdf_link": full_link,
                    "apply_link": "https://psc.wb.gov.in",
                    "apply_btn_text": "WBPSC অনলাইন আবেদন ও OTR পোর্টাল",
                    "apply_status": "অনলাইন আবেদন বিজ্ঞপ্তি অনুযায়ী সক্রিয় হবে",
                    "department": "West Bengal Public Service Commission (WBPSC)",
                    "category": "পশ্চিমবঙ্গ সরকার",
                    "source": "WBPSC"
                })

                if len(notices) >= limit:
                    break

    except Exception as e:
        print(f"[WBPSC] Error scraping: {e}")

    return notices

if __name__ == "__main__":
    results = get_wbpsc_notices()
    print(f"Found {len(results)} WBPSC notices:")
    for r in results:
        print(f"- {r['title']} -> {r['pdf_link']}")
