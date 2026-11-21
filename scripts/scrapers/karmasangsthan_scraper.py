import re
import hashlib
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_drive_url(url):
    """Converts Google Drive view URL to direct streaming/download URL if possible."""
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.usercontent.google.com/u/0/uc?id={file_id}&export=download"
    return url

def get_karmasangsthan_paper():
    """
    Scrapes the latest weekly Karmasangsthan Paper PDF edition from karmasangsthan.online.
    """
    url = "https://karmasangsthan.online/karmasangsthan-paper-karmasangsthan-pdf-karmasangsthan-paper-today/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12, verify=False)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        
        # Look for preview link or table links
        latest_pdf_link = None
        edition_date = "এই সপ্তাহের সংখ্যা"

        # 1. Check direct preview / download links in paragraphs
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            txt = a.get_text(strip=True)
            if "drive.google.com" in href or "drive.usercontent.google.com" in href:
                if not latest_pdf_link:
                    latest_pdf_link = clean_drive_url(href)
                date_match = re.search(r'(\d{1,2}[-\s/]\d{1,2}[-\s/]\d{2,4})', txt)
                if date_match:
                    edition_date = date_match.group(1)
                    latest_pdf_link = clean_drive_url(href)
                    break

        # 2. Check table rows for latest edition date
        table = soup.find("table")
        if table:
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                links = [a["href"] for a in tr.find_all("a", href=True) if "drive" in a["href"]]
                if len(cells) >= 2 and links:
                    edition_date = cells[0].replace("(NEW)", "").strip()
                    latest_pdf_link = clean_drive_url(links[0])
                    break

        if latest_pdf_link:
            title = f"কর্মসংস্থান পেপার (Karmasangsthan Paper) PDF: {edition_date} এই সপ্তাহের সংখ্যা"
            notice_id = f"karmasangsthan_{hashlib.md5(title.encode('utf-8')).hexdigest()[:12]}"
            return {
                "id": notice_id,
                "title": title,
                "official_link": "https://karmasangsthan.online",
                "pdf_link": latest_pdf_link,
                "apply_link": latest_pdf_link,
                "apply_btn_text": "পেপার PDF সরাসরি ডাউনলোড",
                "department": "সাপ্তাহিক কর্মসংস্থান পত্রিকা (Karmasangsthan Weekly)",
                "category": "কর্মসংস্থান পেপার",
                "source": "karmasangsthan.online",
                "vacancies": "একাধিক সরকারি ও বেসরকারি শূন্যপদ",
                "qualification": "৮ম, মাধ্যমিক, উচ্চ মাধ্যমিক ও গ্র্যাজুয়েট পাস",
                "last_date": "বিজ্ঞপ্তি অনুযায়ী নির্ধারিত"
            }
    except Exception as e:
        print(f"[Karmasangsthan] Error fetching paper: {e}")
    return None

def get_karmakshetra_paper():
    """
    Scrapes the latest weekly Karmakshetra Paper PDF from karmasangsthan.online.
    """
    url = "https://karmasangsthan.online/karmakshetra-paper-today/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12, verify=False)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table")
        if table:
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                links = [a["href"] for a in tr.find_all("a", href=True) if "drive" in a["href"]]
                if len(cells) >= 2 and links:
                    edition_date = cells[0].replace("[New]", "").strip()
                    pdf_link = clean_drive_url(links[0])
                    title = f"কর্মক্ষেত্র পেপার (Karmakshetra Paper) PDF: {edition_date} এই সপ্তাহের সংখ্যা"
                    notice_id = f"karmakshetra_{hashlib.md5(title.encode('utf-8')).hexdigest()[:12]}"
                    return {
                        "id": notice_id,
                        "title": title,
                        "official_link": "https://karmasangsthan.online",
                        "pdf_link": pdf_link,
                        "apply_link": pdf_link,
                        "apply_btn_text": "কর্মক্ষেত্র PDF ডাউনলোড করুন",
                        "department": "সাপ্তাহিক কর্মক্ষেত্র পত্রিকা (Karmakshetra Weekly)",
                        "category": "কর্মক্ষেত্র পেপার",
                        "source": "karmasangsthan.online",
                        "vacancies": "রাজ্য ও কেন্দ্রীয় বিভিন্ন পদ",
                        "qualification": "বিভিন্ন যোগ্যতার চাকরি",
                        "last_date": "বিজ্ঞপ্তি অনুযায়ী নির্ধারিত"
                    }
    except Exception as e:
        print(f"[Karmakshetra] Error fetching paper: {e}")
    return None

def get_all_karmasangsthan_notices():
    notices = []
    ks = get_karmasangsthan_paper()
    if ks:
        notices.append(ks)
    kk = get_karmakshetra_paper()
    if kk:
        notices.append(kk)
    return notices

if __name__ == "__main__":
    results = get_all_karmasangsthan_notices()
    print(f"Found {len(results)} newspaper editions:")
    for r in results:
        print(f"- {r['title']}")
        print(f"  PDF: {r['pdf_link']}")
