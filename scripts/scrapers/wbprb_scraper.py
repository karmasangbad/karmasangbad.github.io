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

def get_direct_pdf_link(session, recruitment_url, headers):
    """Fetches the inner recruitment page to extract the direct .pdf download link."""
    try:
        res = session.get(recruitment_url, headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if href.lower().endswith(".pdf") or "/uploads/recruitment/" in href:
                    if href.startswith("/"):
                        return f"https://prb.wb.gov.in{href}"
                    elif href.startswith("http"):
                        return href
                    else:
                        return f"https://prb.wb.gov.in/{href}"
    except Exception as e:
        print(f"[WBPRB] Inner page PDF fetch error: {e}")
    return recruitment_url

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
            href = a["href"].strip()

            if len(title) > 20 and any(k in title.lower() for k in keywords):
                if href.startswith("/"):
                    recruitment_url = f"https://prb.wb.gov.in{href}"
                elif href.startswith("http"):
                    recruitment_url = href
                else:
                    recruitment_url = f"https://prb.wb.gov.in/{href}"

                # Extract the real direct PDF
                pdf_direct_url = get_direct_pdf_link(session, recruitment_url, headers)

                title_lower = title.lower()
                is_admit = "admit" in title_lower or "call letter" in title_lower
                is_result = "result" in title_lower or "merit" in title_lower

                if is_admit:
                    btn_text = "এডমিট কার্ড ডাউনলোড লিঙ্ক"
                    apply_link = "https://wbprb.applythrunet.co.in/"
                    apply_status = ""
                elif is_result:
                    btn_text = "ফলাফল চেক করার পোর্টাল"
                    apply_link = recruitment_url
                    apply_status = ""
                else:
                    btn_text = "অনলাইনে সরাসরি আবেদন করুন"
                    apply_link = "https://wbprb.applythrunet.co.in/"
                    apply_status = ""

                # Deterministic MD5 ID
                notice_id = f"wbprb_{hashlib.md5(title.encode('utf-8')).hexdigest()[:12]}"

                notices.append({
                    "id": notice_id,
                    "title": title,
                    "official_link": "https://prb.wb.gov.in",
                    "pdf_link": pdf_direct_url,
                    "apply_link": apply_link,
                    "apply_btn_text": btn_text,
                    "apply_status": apply_status,
                    "department": "West Bengal Police Recruitment Board (WBPRB)",
                    "category": "Defence & Police",
                    "state": "West Bengal",
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
        print(f"- {r['title']} -> PDF: {r['pdf_link']}")
