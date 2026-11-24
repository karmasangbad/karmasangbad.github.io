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
        try:
            ctx.set_ciphers('DEFAULT:@SECLEVEL=1')
        except:
            pass
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_rrb_notices(limit=8):
    """
    Scrapes the latest notifications from Railway Recruitment Boards (RRB) / Ministry of Railways.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.mount("https://", LegacySSLAdapter())

    notices = []
    
    # 1. Scrape official RRB Portal
    try:
        url = "https://www.rrbkolkata.gov.in"
        response = session.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            keywords = ["cen", "notification", "recruitment", "alp", "technician", "ntpc", "schedule", "results", "selection", "verification"]

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                href = a["href"].strip()

                if len(title) > 5 and ("cennum=" in href.lower() or "cenum=" in href.lower() or "pdf" in href.lower()):
                    if href.startswith("/"):
                        full_link = f"https://www.rrbkolkata.gov.in{href}"
                    elif href.startswith("http"):
                        full_link = href
                    else:
                        full_link = f"https://www.rrbkolkata.gov.in/{href}"

                    clean_title = f"RRB Railway Notification: {title}"
                    notice_id = f"rrb_{hashlib.md5(href.encode('utf-8')).hexdigest()[:12]}"

                    notices.append({
                        "id": notice_id,
                        "title": clean_title,
                        "department": "Railway Recruitment Boards (RRB) / Indian Railways",
                        "category": "Railway Jobs",
                        "state": "All India",
                        "official_link": "https://www.rrbapply.gov.in",
                        "apply_link": "https://www.rrbapply.gov.in",
                        "pdf_link": full_link,
                        "source": "RRB"
                    })

                    if len(notices) >= limit:
                        break
    except Exception as e:
        print(f"[RRB Scraper] Error: {e}")

    return notices

if __name__ == "__main__":
    results = get_rrb_notices()
    print(f"Found {len(results)} RRB notices:")
    for r in results:
        print(f"- {r['title']} -> {r['pdf_link']}")
