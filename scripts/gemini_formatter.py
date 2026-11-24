import os
import re
import json
import requests
from datetime import datetime

def clean_slug(text):
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    return re.sub(r'[\s-]+', '-', text)[:50]

def call_gemini_api(prompt, api_key):
    """
    Calls Gemini API using standard REST endpoint.
    Tries gemini-2.5-flash then gemini-1.5-flash.
    """
    models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048
            }
        }
        headers = {"Content-Type": "application/json"}
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=25)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"[Gemini API] Model {model_name} returned status {res.status_code}: {res.text[:150]}")
        except Exception as e:
            print(f"[Gemini API] Error calling {model_name}: {e}")

    return None

def format_job_to_markdown(notice):
    """
    Takes a raw scraped notice dictionary and returns complete Markdown text with Jekyll YAML frontmatter
    formatted for Pan-India job seekers.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    title = notice.get("title", "")
    department = notice.get("department", "Government of India / State Recruitment Board")
    category = notice.get("category", "Central Govt Jobs")
    state = notice.get("state", "All India")
    official_link = notice.get("official_link", "")
    pdf_link = notice.get("pdf_link", "")
    direct_apply_link = notice.get("apply_link", "")
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0530")

    # Smart button action detection based on title
    custom_btn = notice.get("apply_btn_text")
    custom_status = notice.get("apply_status", "")
    title_lower = title.lower()

    if custom_btn:
        default_btn_text = custom_btn
        default_apply_link = direct_apply_link or pdf_link or official_link
        default_apply_status = custom_status
    elif any(k in title_lower for k in ["admit", "e-admit", "hall ticket"]):
        default_btn_text = "Download Admit Card / Hall Ticket"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["call letter", "personality test", "interview"]):
        default_btn_text = "Download Call Letter / Schedule"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["result", "merit", "cutoff"]):
        default_btn_text = "Check Result & Merit List"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["indicative", "advance", "short notice"]):
        default_btn_text = "Online Application Portal"
        default_apply_link = direct_apply_link or official_link
        default_apply_status = "Online Application Process Starting Soon"
    else:
        default_btn_text = "Apply Online Now"
        default_apply_link = direct_apply_link or pdf_link or official_link
        default_apply_status = ""

    # If GEMINI_API_KEY is available, let AI write a rich Pan-India article
    if api_key:
        prompt = f"""
You are a senior government recruitment editor for India's leading Sarkari job portal (KarmaSangbad).
Analyze this official Indian recruitment notification and write an informative, clear, and attractive job news post in English.

Raw Notification Title: {title}
Department / Organization: {department}
Category: {category}
State / Region: {state}
Official Portal Link: {official_link}
PDF Notification Link: {pdf_link}

Generate a JSON object strictly in this JSON format:
{{
  "title": "Clear English Title for the recruitment (e.g. SSC CGL 2026 Notification: Apply Online for 15,000+ Group B & C Vacancies)",
  "english_slug": "short-english-slug-for-filename",
  "post_name": "Official name of the posts",
  "vacancies": "Total vacancies count or 'Refer Official Notice'",
  "qualification": "Educational qualification required (e.g. 10th Pass / 12th Pass / Graduate Degree)",
  "age_limit": "Age limit (e.g. 18 to 30 years as on prescribed date)",
  "last_date": "Last date to apply or 'Refer Official Notification'",
  "summary": "2-line engaging summary for search engines and social cards",
  "body_markdown": "Full article in Markdown with headings: ## Overview, ## Post & Vacancy Details, ## Eligibility Criteria, ## Application Fee, ## Selection Process, and ## How to Apply Online Step-by-Step."
}}
"""
        response_text = call_gemini_api(prompt, api_key)
        if response_text:
            try:
                clean_json = response_text.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.startswith("```"):
                    clean_json = clean_json[3:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                clean_json = clean_json.strip()

                data = json.loads(clean_json)
                slug = clean_slug(data.get("english_slug", title))
                if not slug:
                    slug = clean_slug(title)

                markdown = f"""---
layout: post
title: "{data.get('title', title)}"
slug: "{slug}"
date: {datetime_str}
department: "{department}"
category: "{category}"
state: "{state}"
vacancies: "{data.get('vacancies', 'Refer Official Notice')}"
qualification: "{data.get('qualification', 'Check Notification')}"
age_limit: "{data.get('age_limit', 'As per rules')}"
last_date: "{data.get('last_date', 'Closing Soon')}"
apply_mode: "Online"
official_link: "{official_link}"
pdf_link: "{pdf_link}"
apply_link: "{default_apply_link}"
apply_btn_text: "{default_btn_text}"
apply_status: "{default_apply_status}"
summary: "{data.get('summary', title)}"
---

{data.get('body_markdown', '')}
"""
                return slug, markdown
            except Exception as e:
                print(f"[Gemini Formatter] JSON parsing error: {e}")

    # Fallback template if Gemini API key is not present or error occurs
    slug = clean_slug(title)
    if not slug:
        slug = f"job-notice-{datetime.now().strftime('%H%M%S')}"

    # Extract qualification hints
    t_low = title.lower()
    if any(k in t_low for k in ["10th", "matric", "secondary"]):
        qual = "10th Pass (Matriculation)"
    elif any(k in t_low for k in ["12th", "inter", "higher secondary"]):
        qual = "12th Pass (Intermediate)"
    elif any(k in t_low for k in ["iti", "diploma", "apprentice"]):
        qual = "ITI / Diploma / Matric"
    elif any(k in t_low for k in ["cgl", "officer", "graduate", "degree"]):
        qual = "Bachelor's Degree (Graduation)"
    else:
        qual = "Check Official Notification"

    markdown = f"""---
layout: post
title: "{title}"
slug: "{slug}"
date: {datetime_str}
department: "{department}"
category: "{category}"
state: "{state}"
vacancies: "Refer Official Notification"
qualification: "{qual}"
age_limit: "As per Govt Norms"
last_date: "Closing Soon"
apply_mode: "Online"
official_link: "{official_link}"
pdf_link: "{pdf_link}"
apply_link: "{default_apply_link}"
apply_btn_text: "{default_btn_text}"
apply_status: "{default_apply_status}"
summary: "{title} - Check detailed eligibility criteria, important dates, official notification PDF, and direct apply link."
---

## Recruitment Overview

**{department}** has published an official recruitment notification for **{title}**. Eligible candidates across India can submit their applications through the official portal before the closing date.

### Important Details Summary

| Particulars | Details |
| :--- | :--- |
| **Conducting Organization** | {department} |
| **Notification Title** | {title} |
| **Category** | {category} |
| **Job Location** | {state} |
| **Eligibility / Qualification** | {qual} |
| **Application Mode** | Online Portal |
| **Official Website** | [{official_link}]({official_link}) |

---

## Eligibility Criteria & Qualifications

1. **Nationality:** Candidate must be a citizen of India.
2. **Educational Qualification:** Candidates should possess recognized educational qualifications from an accredited Board, Council, or University as mandated in the official advertisement.
3. **Age Limit:** Age relaxations are applicable for SC, ST, OBC, PwD, and Ex-Servicemen categories in accordance with Central / State Government reservation guidelines.

---

## How to Apply Online Step-by-Step

1. Visit the official portal: [{official_link}]({official_link}).
2. Locate the link for **{title}** in the latest notices / recruitment section.
3. Download and read the official advertisement carefully to ensure you fulfill all eligibility criteria.
4. Register or log in with your credentials and complete the application form accurately.
5. Upload the required scanned documents (photograph, signature, certificates).
6. Pay the prescribed application fee (if applicable) through online payment modes.
7. Submit the form and download/print a copy of the final application confirmation for future reference.

---

## Important Links & Downloads

* **Official PDF Notification:** [{pdf_link if pdf_link else official_link}]({pdf_link if pdf_link else official_link})
* **Direct Application Portal:** [{default_apply_link}]({default_apply_link})
* **Official Website:** [{official_link}]({official_link})
"""
    return slug, markdown

# Backwards compatibility alias
format_job_to_bengali_markdown = format_job_to_markdown
