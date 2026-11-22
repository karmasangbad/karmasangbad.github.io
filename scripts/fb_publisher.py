import os
import sys
import shutil
import tempfile
import subprocess
import requests

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
BANNERS_DIR = os.path.join(BASE_DIR, "assets", "banners")
os.makedirs(BANNERS_DIR, exist_ok=True)

def find_browser_executable():
    """Finds available Chrome or Edge browser on Windows or Linux."""
    # Check PATH first
    for name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium", "chrome", "msedge"]:
        path = shutil.which(name)
        if path:
            return path

    # Common Windows paths
    win_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for p in win_paths:
        if os.path.exists(p):
            return p

    # Common Linux paths
    linux_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]
    for p in linux_paths:
        if os.path.exists(p):
            return p

    return None

def generate_fb_banner(notice, slug):
    """
    Generates a 1200x630 Facebook banner image with Bengali typography.
    Returns the path to the generated PNG image.
    """
    title = notice.get("title", "সরকারি চাকরির খবর")
    department = notice.get("department", "Government Organization")
    category = notice.get("category", "পশ্চিমবঙ্গ সরকার")
    vacancies = notice.get("vacancies", "বিজ্ঞপ্তি দেখুন")
    qualification = notice.get("qualification", "নোটিফিকেশন দেখুন")
    last_date = notice.get("last_date", "শীঘ্রই সমাপ্ত")

    html_content = f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      width: 1200px;
      height: 630px;
      font-family: 'Hind Siliguri', sans-serif;
      background: linear-gradient(135deg, #091a28 0%, #0f3d3e 50%, #064e3b 100%);
      color: #ffffff;
      padding: 45px 55px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      background: #22c55e;
      color: #091a28;
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      font-weight: bold;
    }}
    .brand-name {{
      font-size: 26px;
      font-weight: 700;
      color: #ffffff;
    }}
    .brand-tag {{
      color: #4ade80;
    }}
    .category-badge {{
      background: rgba(34, 197, 94, 0.2);
      border: 1.5px solid #22c55e;
      color: #4ade80;
      padding: 6px 18px;
      border-radius: 30px;
      font-size: 18px;
      font-weight: 600;
    }}
    .main-content {{
      margin: 15px 0;
    }}
    .dept-title {{
      font-size: 20px;
      color: #94a3b8;
      font-weight: 600;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .job-title {{
      font-size: 38px;
      font-weight: 700;
      line-height: 1.25;
      color: #ffffff;
      text-shadow: 0 2px 10px rgba(0,0,0,0.4);
      margin-bottom: 25px;
      max-height: 110px;
      overflow: hidden;
    }}
    .highlights-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .card {{
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 14px;
      padding: 14px 18px;
    }}
    .card-label {{
      font-size: 15px;
      color: #cbd5e1;
      margin-bottom: 4px;
    }}
    .card-value {{
      font-size: 20px;
      font-weight: 700;
      color: #fef08a;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 15px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
    }}
    .website-url {{
      font-size: 20px;
      color: #38bdf8;
      font-weight: 600;
    }}
    .cta-btn {{
      background: #22c55e;
      color: #0f172a;
      font-size: 18px;
      font-weight: 700;
      padding: 10px 24px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">
      <div class="brand-icon">💼</div>
      <div class="brand-name">চাকরির <span class="brand-tag">খবর</span> (KarmaSangbad)</div>
    </div>
    <div class="category-badge">{category}</div>
  </div>

  <div class="main-content">
    <div class="dept-title">{department}</div>
    <div class="job-title">{title}</div>

    <div class="highlights-grid">
      <div class="card">
        <div class="card-label">মোট শূন্যপদ:</div>
        <div class="card-value">{vacancies}</div>
      </div>
      <div class="card">
        <div class="card-label">শিক্ষাগত যোগ্যতা:</div>
        <div class="card-value">{qualification}</div>
      </div>
      <div class="card">
        <div class="card-label">আবেদনের শেষ তারিখ:</div>
        <div class="card-value" style="color: #f87171;">{last_date}</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="website-url">🌐 সম্পূর্ণ তথ্য ও আবেদন: karmasangbad.github.io</div>
    <div class="cta-btn">অনলাইনে আবেদন লিঙ্ক ➔</div>
  </div>
</body>
</html>
"""
    output_png = os.path.join(BANNERS_DIR, f"{slug}.png")

    # Render via headless browser
    browser_exe = find_browser_executable()
    if not browser_exe:
        print("[FB Banner] Warning: No Chrome/Edge browser found. Skipping banner render.")
        return None

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_content)
        temp_html_path = tf.name

    try:
        cmd = [
            browser_exe,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size=1200,630",
            f"--screenshot={output_png}",
            f"file:///{temp_html_path.replace(os.sep, '/')}"
        ]
        subprocess.run(cmd, capture_output=True, timeout=20)
        if os.path.exists(output_png) and os.path.getsize(output_png) > 1000:
            print(f"[FB Banner] Successfully generated: assets/banners/{slug}.png")
            return output_png
    except Exception as e:
        print(f"[FB Banner] Render error: {e}")
    finally:
        if os.path.exists(temp_html_path):
            try:
                os.remove(temp_html_path)
            except:
                pass

    return None

def post_to_facebook_page(image_path, caption):
    """
    Uploads a photo with description and article link to Facebook Page via Graph API.
    """
    page_id = os.environ.get("FB_PAGE_ID", "61596771963967").strip()
    access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN", "").strip()

    if not page_id or not access_token:
        print("[Facebook Bot] FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN not set in environment. Skipping Facebook post.")
        return False

    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
    payload = {
        "caption": caption,
        "access_token": access_token
    }

    try:
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files, timeout=30)
            
        data = response.json()
        if response.status_code == 200 and "id" in data:
            print(f"[Facebook Bot] Successfully published to Facebook! Post ID: {data['id']}")
            return True
        else:
            print(f"[Facebook Bot] Error posting to Facebook ({response.status_code}): {data}")
            return False
    except Exception as e:
        print(f"[Facebook Bot] Request error: {e}")
        return False

def auto_publish_job_to_fb(notice, article_url, slug):
    """
    Generates banner and publishes to Facebook Page.
    """
    title = notice.get("title", "নতুন সরকারি চাকরির বিজ্ঞপ্তি")
    department = notice.get("department", "সরকারি দপ্তর")
    vacancies = notice.get("vacancies", "বিজ্ঞপ্তি অনুযায়ী")
    qualification = notice.get("qualification", "নোটিফিকেশন দেখুন")
    last_date = notice.get("last_date", "শীঘ্রই সমাপ্ত")

    banner_path = generate_fb_banner(notice, slug)
    if not banner_path:
        print("[Facebook Bot] Could not create banner image.")
        return False

    caption = f"""📢 নতুন সরকারি চাকরির বিজ্ঞপ্তি প্রকাশিত হয়েছে!

📌 পদের নাম: {title}
🏛 দপ্তর/সংস্থা: {department}
👥 মোট শূন্যপদ: {vacancies}
🎓 শিক্ষাগত যোগ্যতা: {qualification}
🗓 আবেদনের শেষ তারিখ: {last_date}

👉 কীভাবে ধাপে ধাপে আবেদন করবেন এবং অফিশিয়াল নোটিফিকেশন PDF ডাউনলোড করতে নিচের লিংকে ক্লিক করুন:
🔗 {article_url}

#পশ্চিমবঙ্গ_চাকরি #সরকারি_চাকরি #WBJobs #KarmaSangbad #GovtJobs #JobAlert
"""
    return post_to_facebook_page(banner_path, caption)

if __name__ == "__main__":
    sample_notice = {
        "title": "পশ্চিমবঙ্গ পুলিশ কনস্টেবল ও লেডি কনস্টেবল নিয়োগ ২০২৬",
        "department": "West Bengal Police Recruitment Board (WBPRB)",
        "category": "পুলিশ ও ডিফেন্স",
        "vacancies": "১০,০০০+ পদ",
        "qualification": "মাধ্যমিক পাস",
        "last_date": "২০ জানুয়ারি ২০২৭"
    }
    banner = generate_fb_banner(sample_notice, "sample_test_job")
    print("Test banner created at:", banner)
