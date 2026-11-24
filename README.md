# KarmaSangbad - All India Govt Job News & Sarkari Recruitment Portal

An automated, modern Government Job Recruitment portal covering **Central Government & All Indian States** (UPSC, SSC, Indian Railways / RRB, Banking / IBPS & SBI, Defence & Police, State PSCs, and Employment News). Built with **Jekyll**, hosted 100% free on **GitHub Pages**, and powered by daily **GitHub Actions** automation with **Facebook Page Auto-Posting**.

---

## 🌟 Key Features

1. **Pan-India Coverage:**
   - **Central Government:** UPSC (Civil Services, NDA, CDS), SSC (CGL, CHSL, MTS, GD Constable), Employment News India.
   - **Indian Railways (RRB):** Assistant Loco Pilot (ALP), Technician, NTPC, Group D, Junior Engineer.
   - **Banking & Finance:** IBPS (PO, Clerk, SO, RRB), State Bank of India (SBI), RBI.
   - **Defence & Police:** Indian Army (Agniveer), Indian Navy, Indian Air Force, Central Armed Police Forces (CAPF), State Police Boards.
   - **State Government Jobs:** West Bengal, Uttar Pradesh, Bihar, Delhi/NCR, Maharashtra, Rajasthan, South States, etc.
   - **Jobs by Qualification:** 10th Pass (Matriculation), 12th Pass (Intermediate), ITI / Diploma, Graduate Degree, Post Graduate.
2. **100% Free Cloud Infrastructure:**
   - Zero hosting or server cost running on **GitHub Pages**.
   - Automated daily scraping and publishing at 6:00 AM IST via **GitHub Actions**.
3. **Facebook Auto-Publisher with Dynamic Banners:**
   - Generates high-contrast 1200x630 recruitment banners using headless Chrome/Edge.
   - Publishes image banners with captions and direct article links to Facebook Page via Meta Graph API.
4. **Google Jobs SEO & Mobile Responsive:**
   - Schema.org `JobPosting` structured JSON-LD for rich snippets on Google Search.
   - Fast instant search and sector/state filters using Tailwind CSS.
   - Official direct PDF download links and active online apply buttons.

---

## 📁 Repository Structure

```
├── .github/workflows/
│   ├── daily_job_bot.yml      # Cron automation (Daily 6:00 AM IST)
│   └── deploy.yml             # GitHub Pages automated deployment
├── _includes/
│   ├── header.html            # Top banner, Pan-India nav, social links
│   ├── footer.html            # Disclaimer, categories, copyright
│   ├── head.html              # Typography (Inter, Poppins, Hind Siliguri)
│   └── schema.html            # Schema.org JobPosting JSON-LD
├── _layouts/
│   ├── default.html           # Master layout
│   ├── home.html              # Hero, live search, sector/state filters
│   └── post.html              # Job details, official links & PDF downloads
├── _posts/                    # Published recruitment notices
├── assets/
│   ├── js/search.js           # Live search and multi-state filter logic
│   └── banners/               # Generated social media banners
├── scripts/
│   ├── runner.py              # Orchestrates scrapers and publisher
│   ├── gemini_formatter.py    # Formats notices into structured Markdown
│   ├── fb_publisher.py        # Generates banners and posts to Facebook
│   └── scrapers/
│       ├── upsc_scraper.py    # Union Public Service Commission
│       ├── ssc_scraper.py     # Staff Selection Commission
│       ├── rrb_scraper.py     # Railway Recruitment Boards
│       ├── bank_scraper.py    # IBPS & SBI Banking
│       ├── employment_news_scraper.py # Employment News India
│       ├── wbpsc_scraper.py   # State PSCs
│       ├── wbprb_scraper.py   # State Police Boards
│       └── karmasangsthan_scraper.py # Weekly recruitment newspapers
├── _config.yml                # Site configuration and social channels
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Secrets Configuration (GitHub Actions)

Add the following under **Settings > Secrets and variables > Actions**:

| Secret Name | Description |
| :--- | :--- |
| `GEMINI_API_KEY` | *(Optional)* Google Gemini API key for AI writing |
| `FB_PAGE_ID` | Facebook Page ID (e.g. `1586846211175136`) |
| `FB_PAGE_ACCESS_TOKEN` | Facebook Page Access Token with `pages_manage_posts` & `pages_read_engagement` |
