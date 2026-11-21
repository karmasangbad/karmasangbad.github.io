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
    Calls Gemini API using standard REST endpoint (lightweight, zero dependency issues).
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
            res = requests.post(url, json=payload, headers=headers, timeout=30)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"[Gemini API] Model {model_name} returned status {res.status_code}: {res.text[:200]}")
        except Exception as e:
            print(f"[Gemini API] Error calling {model_name}: {e}")

    return None

def format_job_to_bengali_markdown(notice):
    """
    Takes a raw scraped notice dictionary and returns complete Markdown text with Jekyll YAML frontmatter.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    title = notice.get("title", "")
    department = notice.get("department", "Government Organization")
    category = notice.get("category", "পশ্চিমবঙ্গ সরকার")
    official_link = notice.get("official_link", "")
    pdf_link = notice.get("pdf_link", "")
    direct_apply_link = notice.get("apply_link", "")
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0530")

    # Smart button action detection based on title
    title_lower = title.lower()
    if any(k in title_lower for k in ["admit", "e-admit"]):
        default_btn_text = "এডমিট কার্ড ডাউনলোড লিঙ্ক"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["call letter", "personality test"]):
        default_btn_text = "কল লেটার ডাউনলোড লিঙ্ক"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["result", "merit"]):
        default_btn_text = "ফলাফল / মেরিট লিস্ট দেখুন"
        default_apply_link = pdf_link or official_link
        default_apply_status = ""
    elif any(k in title_lower for k in ["indicative", "advance"]):
        default_btn_text = "অনলাইন আবেদন পোর্টাল"
        default_apply_link = direct_apply_link or official_link
        default_apply_status = "অনলাইন আবেদন প্রক্রিয়া শীঘ্রই শুরু হবে"
    else:
        default_btn_text = "অনলাইনে আবেদন করুন"
        default_apply_link = direct_apply_link or pdf_link or official_link
        default_apply_status = ""

    # If GEMINI_API_KEY is available, let AI write a rich Bengali article
    if api_key:
        prompt = f"""
You are a senior Bengali government job news editor for a leading job portal (KarmaSangbad).
Analyze the following official Indian recruitment notification and write an informative, attractive Bengali job news post.

Raw Notification Title: {title}
Department / Organization: {department}
Category: {category}
Official Portal Link: {official_link}
PDF Notification Link: {pdf_link}

Generate a JSON object strictly in this JSON format:
{{
  "bengali_title": "Attractive Bengali title for the job update (e.g. পশ্চিমবঙ্গ ... পদে নতুন নিয়োগ বিজ্ঞপ্তি ২০২৬)",
  "english_slug": "short-english-slug-for-filename",
  "post_name": "Name of the post in Bengali",
  "vacancies": "Estimated vacancy or 'অফিশিয়াল বিজ্ঞপ্তিতে দেখুন'",
  "qualification": "Educational qualification required in Bengali (e.g. মাধ্যমিক / উচ্চ মাধ্যমিক / স্নাতক পাস)",
  "age_limit": "Age limit in Bengali (e.g. ১৮ থেকে ৪০ বছর)",
  "last_date": "Last date to apply in Bengali or 'শীঘ্রই সমাপ্ত'",
  "apply_mode": "অনলাইন (Online) / অফলাইন",
  "apply_btn_text": "অনলাইনে আবেদন করুন / এডমিট কার্ড ডাউনলোড / নোটিফিকেশন পোর্টাল",
  "apply_status": "Status if upcoming e.g. 'আবেদন শীঘ্রই শুরু হবে' or empty string if active",
  "summary": "1-2 sentence Bengali summary for social media preview",
  "body_content": "Detailed Bengali body content in clean Markdown including:
    - নিয়োগ সংক্রান্ত সারসংক্ষেপ
    - শিক্ষাগত যোগ্যতা ও বয়সসীমা
    - নির্বাচন পদ্ধতি (Selection Process)
    - ধাপে ধাপে অনলাইনে আবেদন করার সম্পূর্ণ নির্দেশিকা (Step-by-step How to Apply in Bengali)
    - আবেদন ফি ও অন্যান্য নিয়মাবলী"
}}

Respond ONLY with the raw JSON object, without backticks or markdown fences.
"""
        response_text = call_gemini_api(prompt, api_key)
        if response_text:
            try:
                cleaned_json = re.sub(r'^```json\s*', '', response_text.strip(), flags=re.MULTILINE)
                cleaned_json = re.sub(r'```$', '', cleaned_json.strip())
                parsed = json.loads(cleaned_json)

                bengali_title = parsed.get("bengali_title", title)
                slug = clean_slug(parsed.get("english_slug", title))
                post_name = parsed.get("post_name", title)
                vacancies = parsed.get("vacancies", "অফিশিয়াল বিজ্ঞপ্তিতে দেখুন")
                qualification = parsed.get("qualification", "অফিশিয়াল বিজ্ঞপ্তিতে বিস্তারিত")
                age_limit = parsed.get("age_limit", "নিয়মানুযায়ী ছাড় প্রযোজ্য")
                last_date = parsed.get("last_date", "শীঘ্রই সমাপ্ত")
                apply_mode = parsed.get("apply_mode", "অনলাইন (Online)")
                apply_btn_text = parsed.get("apply_btn_text", default_btn_text)
                apply_status = parsed.get("apply_status", default_apply_status)
                summary = parsed.get("summary", bengali_title)
                body = parsed.get("body_content", "")

                status_yaml = f'apply_status: "{apply_status}"' if apply_status else ""

                markdown = f"""---
layout: post
title: "{bengali_title}"
date: {datetime_str}
category: "{category}"
tags: ["{category}", "{department}"]
department: "{department}"
post_name: "{post_name}"
vacancies: "{vacancies}"
qualification: "{qualification}"
age_limit: "{age_limit}"
last_date: "{last_date}"
apply_mode: "{apply_mode}"
apply_btn_text: "{apply_btn_text}"
{status_yaml}
official_link: "{official_link}"
pdf_link: "{pdf_link}"
apply_link: "{default_apply_link}"
summary: "{summary}"
---

{body}
"""
                return slug, markdown
            except Exception as err:
                print(f"[Gemini Formatter] JSON parsing error: {err}. Falling back to default template.")

    # Fallback template if no API key or AI call failed
    slug = clean_slug(title)
    bengali_title = f"{department}: {title[:80]}"
    status_yaml = f'apply_status: "{default_apply_status}"' if default_apply_status else ""

    markdown = f"""---
layout: post
title: "{bengali_title}"
date: {datetime_str}
category: "{category}"
tags: ["{category}", "{department}"]
department: "{department}"
post_name: "{title[:70]}"
vacancies: "বিজ্ঞপ্তি অনুযায়ী নির্ধারিত"
qualification: "অফিশিয়াল নোটিফিকেশন দেখুন"
age_limit: "সরকারি নিয়ম অনুযায়ী প্রযোজ্য"
last_date: "অফিশিয়াল বিজ্ঞপ্তিতে দেখুন"
apply_mode: "অনলাইন (Online)"
apply_btn_text: "{default_btn_text}"
{status_yaml}
official_link: "{official_link}"
pdf_link: "{pdf_link}"
apply_link: "{default_apply_link}"
summary: "{bengali_title} সংক্রান্ত নতুন অফিশিয়াল নোটিফিকেশন ও নির্দেশিকা।"
---

{department}-এর পক্ষ থেকে নতুন চাকরির বিজ্ঞপ্তি প্রকাশিত হয়েছে। আগ্রহী চাকরিপ্রার্থীরা নিচে দেওয়া নিয়ম মেনে আবেদন করতে পারেন।

## নিয়োগ সংক্রান্ত সংক্ষিপ্ত বিবরণ:
* **সংস্থা:** {department}
* **বিজ্ঞপ্তির বিষয়:** {title}
* **অফিশিয়াল ওয়েবসাইট:** [{official_link}]({official_link})

## শিক্ষাগত যোগ্যতা ও অন্যান্য শর্তাবলী:
প্রার্থীদের শিক্ষাগত যোগ্যতা, বয়সসীমা এবং অন্যান্য আবশ্যিক যোগ্যতার বিস্তারিত তথ্যের জন্য অফিশিয়াল নোটিফিকেশন PDF ডাউনলোড করে দেখে নেওয়ার অনুরোধ জানানো হচ্ছে।

## কীভাবে অনলাইনে আবেদন করবেন (How to Apply):
1. প্রথমে অফিশিয়াল পোর্টালে যান: [{official_link}]({official_link})
2. সংশ্লিষ্ট বিজ্ঞপ্তির লিংক খুঁজে বের করে 'Apply Online' বাটনে ক্লিক করুন।
3. মোবাইল নম্বর ও ইমেল আইডি দিয়ে রেজিস্ট্রেশন সম্পন্ন করুন।
4. সমস্ত ব্যক্তিগত ও শিক্ষাগত তথ্যের ঘর সঠিকভাবে পূরণ করুন।
5. প্রয়োজনীয় নথি এবং ছবি আপলোড করুন।
6. আবেদন ফি প্রযোজ্য হলে জমা দিয়ে ফাইনাল সাবমিট করুন এবং আবেদনপত্রের কপি প্রিন্ট করে রাখুন।
"""
    return slug, markdown
