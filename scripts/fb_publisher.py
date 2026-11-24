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
    for name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium", "chrome", "msedge"]:
        path = shutil.which(name)
        if path:
            return path

    win_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for p in win_paths:
        if os.path.exists(p):
            return p

    linux_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]
    for p in linux_paths:
        if os.path.exists(p):
            return p

    return None

def generate_fb_banner(notice, slug):
    """
    Generates a 1200x630 Facebook banner image with modern typography.
    Returns the path to the generated PNG image.
    """
    title = notice.get("title", "Government Job Recruitment")
    department = notice.get("department", "Government Organization")
    category = notice.get("category", "All India Govt Jobs")
    state = notice.get("state", "All India")
    vacancies = notice.get("vacancies", "Refer Notice")
    qualification = notice.get("qualification", "Check Notification")
    last_date = notice.get("last_date", "Closing Soon")

    output_filename = f"fb_{slug}.png"
    output_path = os.path.join(BANNERS_DIR, output_filename)

    browser_bin = find_browser_executable()
    if not browser_bin:
        print("[FB Banner] Chrome/Chromium/Edge browser not found. Skipping banner generation.")
        return None

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Poppins:wght@700;800&family=Hind+Siliguri:wght@600;700&display=swap" rel="stylesheet">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      width: 1200px;
      height: 630px;
      overflow: hidden;
      font-family: 'Inter', 'Hind Siliguri', sans-serif;
      background: linear-gradient(135deg, #091e17 0%, #064e3b 50%, #0f172a 100%);
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 45px 55px;
      position: relative;
    }}
    .bg-accent {{
      position: absolute;
      top: -100px;
      right: -100px;
      width: 450px;
      height: 450px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(0,0,0,0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }}
    .bg-accent-bottom {{
      position: absolute;
      bottom: -150px;
      left: -100px;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(6, 95, 70, 0.3) 0%, rgba(0,0,0,0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }}
    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      width: 44px;
      height: 44px;
      background: #10b981;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 22px;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }}
    .brand-name {{
      font-family: 'Poppins', sans-serif;
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}
    .brand-name span {{
      color: #34d399;
    }}
    .category-badge {{
      background: rgba(16, 185, 129, 0.2);
      border: 1.5px solid #10b981;
      color: #6ee7b7;
      padding: 6px 20px;
      border-radius: 30px;
      font-size: 17px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .main-content {{
      margin: 15px 0;
      z-index: 10;
    }}
    .dept-title {{
      font-size: 20px;
      color: #94a3b8;
      font-weight: 600;
      margin-bottom: 8px;
      letter-spacing: 0.5px;
    }}
    .job-title {{
      font-family: 'Poppins', 'Hind Siliguri', sans-serif;
      font-size: 38px;
      font-weight: 800;
      line-height: 1.25;
      color: #ffffff;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
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
      padding: 14px 20px;
    }}
    .card-label {{
      font-size: 14px;
      color: #cbd5e1;
      margin-bottom: 4px;
      font-weight: 500;
    }}
    .card-value {{
      font-size: 20px;
      font-weight: 700;
      color: #fef08a;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 15px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      z-index: 10;
    }}
    .website-url {{
      font-size: 18px;
      color: #a7f3d0;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}
    .apply-badge {{
      background: linear-gradient(90deg, #10b981 0%, #059669 100%);
      color: #ffffff;
      padding: 10px 24px;
      border-radius: 10px;
      font-size: 17px;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }}
  </style>
</head>
<body>
  <div class="bg-accent"></div>
  <div class="bg-accent-bottom"></div>

  <div class="header">
    <div class="brand-logo">
      <div class="brand-icon">💼</div>
      <div class="brand-name">Karma<span>Sangbad</span></div>
    </div>
    <div class="category-badge">{category}</div>
  </div>

  <div class="main-content">
    <div class="dept-title">{department} • {state}</div>
    <div class="job-title">{title}</div>
    
    <div class="highlights-grid">
      <div class="card">
        <div class="card-label">Total Vacancies</div>
        <div class="card-value">{vacancies}</div>
      </div>
      <div class="card">
        <div class="card-label">Educational Qualification</div>
        <div class="card-value">{qualification}</div>
      </div>
      <div class="card">
        <div class="card-label">Last Date to Apply</div>
        <div class="card-value" style="color: #f87171;">{last_date}</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="website-url">🌐 karmasangbad.github.io • All India Govt Job News</div>
    <div class="apply-badge">Apply Online Now →</div>
  </div>
</body>
</html>
"""

    temp_html_fd, temp_html_path = tempfile.mkstemp(suffix=".html", prefix="fb_card_")
    with os.fdopen(temp_html_fd, "w", encoding="utf-8") as f:
        f.write(html_content)

    try:
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--window-size=1200,630",
            f"--screenshot={output_path}",
            f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[FB Banner] Successfully generated banner: {output_path}")
            return output_path
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
    page_id = os.environ.get("FB_PAGE_ID", "1586846211175136").strip()
    access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN", "").strip()

    if not access_token:
        print("[Facebook Bot] FB_PAGE_ACCESS_TOKEN not set in environment. Skipping Facebook post.")
        return False

    # Using {page_id}/photos or me/photos with Page Access Token
    url = f"https://graph.facebook.com/v19.0/{page_id}/photos" if page_id else "https://graph.facebook.com/v19.0/me/photos"
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
    Generates banner and publishes to Facebook Page for All India audiences.
    """
    title = notice.get("title", "New Government Job Recruitment")
    department = notice.get("department", "Government Organization")
    category = notice.get("category", "All India Govt Jobs")
    state = notice.get("state", "All India")
    vacancies = notice.get("vacancies", "Refer Notification")
    qualification = notice.get("qualification", "Check Notification")
    last_date = notice.get("last_date", "Closing Soon")

    banner_path = generate_fb_banner(notice, slug)
    if not banner_path:
        print("[Facebook Bot] Could not create banner image.")
        return False

    caption = f"""📢 NEW GOVT JOB RECRUITMENT NOTIFICATION OUT!

📌 Post: {title}
🏛 Organization: {department}
🗺 Location: {state}
👥 Total Vacancies: {vacancies}
🎓 Eligibility: {qualification}
🗓 Last Date to Apply: {last_date}

👉 Step-by-step application procedure, eligibility criteria & direct PDF notification download:
🔗 {article_url}

#GovtJobs #SarkariNaukri #AllIndiaJobs #JobAlert #CentralGovtJobs #RailwayJobs #BankJobs #SSC #UPSC #Recruitment2026
"""
    return post_to_facebook_page(banner_path, caption)

if __name__ == "__main__":
    sample_notice = {
        "title": "SSC CGL 2026: Apply Online for 15,000+ Group B & C Posts",
        "department": "Staff Selection Commission (SSC)",
        "category": "Central Govt Jobs",
        "state": "All India",
        "vacancies": "15,000+ Posts",
        "qualification": "Graduate in any discipline",
        "last_date": "30 January 2027"
    }
    banner = generate_fb_banner(sample_notice, "sample_all_india_test")
    print("Test banner created at:", banner)
