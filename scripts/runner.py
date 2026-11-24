import os
import sys
import json
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Ensure scripts directory is in python module search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from scrapers.ssc_scraper import get_ssc_notices
from scrapers.upsc_scraper import get_upsc_notices
from scrapers.rrb_scraper import get_rrb_notices
from scrapers.bank_scraper import get_bank_notices
from scrapers.employment_news_scraper import get_employment_news_notices
from scrapers.wbpsc_scraper import get_wbpsc_notices
from scrapers.wbprb_scraper import get_wbprb_notices
from scrapers.karmasangsthan_scraper import get_all_karmasangsthan_notices
from gemini_formatter import format_job_to_markdown
from fb_publisher import auto_publish_job_to_fb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "_posts")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Runner] Error loading history: {e}")
    return {"seen_ids": []}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def run_pipeline():
    os.makedirs(POSTS_DIR, exist_ok=True)
    history = load_history()
    seen_ids = set(history.get("seen_ids", []))

    print(f"[Runner] Loaded {len(seen_ids)} previously processed notices.")
    print("[Runner] Starting All-India scraping from Central & State official portals...")

    all_notices = []
    
    # 1. Staff Selection Commission (SSC) - Central
    try:
        ssc = get_ssc_notices(limit=5)
        print(f"[Runner] Fetched {len(ssc)} notices from SSC.")
        all_notices.extend(ssc)
    except Exception as e:
        print(f"[Runner] SSC error: {e}")

    # 2. Union Public Service Commission (UPSC) - Central
    try:
        upsc = get_upsc_notices(limit=5)
        print(f"[Runner] Fetched {len(upsc)} notices from UPSC.")
        all_notices.extend(upsc)
    except Exception as e:
        print(f"[Runner] UPSC error: {e}")

    # 3. Railway Recruitment Boards (RRB) - Central / Railways
    try:
        rrb = get_rrb_notices(limit=5)
        print(f"[Runner] Fetched {len(rrb)} notices from RRB.")
        all_notices.extend(rrb)
    except Exception as e:
        print(f"[Runner] RRB error: {e}")

    # 4. Banking & Financial Sector (IBPS) - Central / Banking
    try:
        banks = get_bank_notices(limit=5)
        print(f"[Runner] Fetched {len(banks)} notices from IBPS.")
        all_notices.extend(banks)
    except Exception as e:
        print(f"[Runner] IBPS error: {e}")

    # 5. Employment News India - Central
    try:
        emp = get_employment_news_notices(limit=5)
        print(f"[Runner] Fetched {len(emp)} notices from Employment News.")
        all_notices.extend(emp)
    except Exception as e:
        print(f"[Runner] Employment News error: {e}")

    # 6. West Bengal Public Service Commission (WBPSC) - State
    try:
        wbpsc = get_wbpsc_notices(limit=5)
        print(f"[Runner] Fetched {len(wbpsc)} notices from WBPSC.")
        all_notices.extend(wbpsc)
    except Exception as e:
        print(f"[Runner] WBPSC error: {e}")

    # 7. West Bengal Police Recruitment Board (WBPRB) - State Defence & Police
    try:
        wbprb = get_wbprb_notices(limit=5)
        print(f"[Runner] Fetched {len(wbprb)} notices from WBPRB.")
        all_notices.extend(wbprb)
    except Exception as e:
        print(f"[Runner] WBPRB error: {e}")

    # 8. Weekly Job Newspapers (Karmasangsthan & Karmakshetra)
    try:
        ks_papers = get_all_karmasangsthan_notices()
        print(f"[Runner] Fetched {len(ks_papers)} editions from weekly papers.")
        all_notices.extend(ks_papers)
    except Exception as e:
        print(f"[Runner] Weekly papers error: {e}")

    new_posts_count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    for notice in all_notices:
        nid = notice.get("id")
        if not nid or nid in seen_ids:
            continue

        print(f"[Runner] Processing new notice: {notice['title'][:60]}...")
        slug, markdown_content = format_job_to_markdown(notice)

        filename = f"{today_str}-{slug}.md"
        filepath = os.path.join(POSTS_DIR, filename)

        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(POSTS_DIR, f"{today_str}-{slug}-{counter}.md")
            counter += 1

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"[Runner] Saved: _posts/{os.path.basename(filepath)}")

        article_url = f"https://karmasangbad.github.io/"
        try:
            auto_publish_job_to_fb(notice, article_url, slug)
        except Exception as fb_err:
            print(f"[Runner] Facebook post error: {fb_err}")

        seen_ids.add(nid)
        new_posts_count += 1

    history["seen_ids"] = list(seen_ids)
    save_history(history)
    print(f"[Runner] Completed successfully. {new_posts_count} new job articles published.")

if __name__ == "__main__":
    run_pipeline()
