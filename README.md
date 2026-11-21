# KarmaSangbad (চাকরির খবর) - Automated Bengali Govt Job Portal

একটি সম্পূর্ণ স্বয়ংক্রিয় (Fully Automated) সরকারি চাকরির খবর ওয়েবসাইট, যা প্রতিদিন পশ্চিমবঙ্গ (WBPSC, WBPRB) এবং কেন্দ্রীয় সরকার (SSC, Employment News, রেলওয়ে)-এর অফিশিয়াল নোটিফিকেশন সংগ্রহ করে, বাংলায় সহজ ভাষায় আবেদন নির্দেশিকাসহ প্রকাশ করে।

---

## 🌟 প্রধান বৈশিষ্ট্যসমূহ (Key Features):
1. **১০০% বিনামূল্যে হোস্টিং ও অটোমেশন (GitHub Pages & Actions):** কোনো পেইড হোস্টিং বা সার্ভার ফি দিতে হবে না।
2. **প্রতিদিনের অটোমেটিক আপডেট:** প্রতিদিন সকাল ৬:০০ টায় GitHub Actions স্বয়ংক্রিয়ভাবে নোটিফিকেশন চেক ও প্রকাশ করে।
3. **AI দ্বারা বাংলায় রূপান্তর ও নির্দেশিকা:** Google Gemini AI নোটিফিকেশন বিশ্লেষণ করে বাংলায় সহজবোধ্য আবেদন পদ্ধতি (How to Apply) প্রস্তুত করে।
4. **অফিসিয়াল লিঙ্ক ও PDF নোটিফিকেশন:** সরাসরি আবেদন ও অফিশিয়াল নোটিফিকেশন ডাউনলোড লিঙ্ক যুক্ত থাকে।
5. **SEO ও মোবাইল ফ্রেন্ডলি:** 
   - পরিষ্কার বাংলা ফন্ট (`Hind Siliguri`).
   - Google Job Search এর জন্য Schema.org (`JobPosting`) স্ট্রাকচার্ড ডেটা।
   - লাইভ ইনস্ট্যান্ট সার্চ এবং ক্যাটাগরি ফিল্টার (পশ্চিমবঙ্গ, কেন্দ্রীয়, পুলিশ)।
   - হোয়াটসঅ্যাপ ও টেলিগ্রাম শেয়ার বাটন।

---

## 🚀 সেটআপ ও চালু করার নির্দেশিকা (3-Step Quick Setup):

### ধাপ ১: GitHub-এ রিপোজিটরি তৈরি ও পুশ করুন
আপনার কম্পিউটারের টার্মিনাল বা PowerShell-এ এই ফোল্ডারে গিয়ে কমান্ডগুলো চালান:

```bash
git init
git add .
git commit -m "Initial commit for KarmaSangbad Bengali Job Portal"
git branch -M main
git remote add origin https://github.com/<আপনার-ইউজারনেম>/<রিপোজিটরি-নাম>.git
git push -u origin main
```

---

### ধাপ ২: GitHub Pages চালু করুন (Enable Pages)
1. আপনার GitHub রিপোজিটরির **Settings** ট্যাবে যান।
2. বাঁদিকের মেনু থেকে **Pages** সিলেক্ট করুন।
3. **Build and deployment > Source** অপশনে **GitHub Actions** নির্বাচন করুন।
4. ব্যস! রিপোজিটরিতে কোনো পরিবর্তন বা নতুন পোস্ট এলেই স্বয়ংক্রিয়ভাবে ওয়েবসাইট লাইভ হয়ে যাবে। আপনার ওয়েবসাইটের লিঙ্ক হবে:
   `https://<আপনার-ইউজারনেম>.github.io/<রিপোজিটরি-নাম>/`

---

### ধাপ ৩: Gemini API Key যুক্ত করুন (Free AI Writer)
1. [Google AI Studio](https://aistudio.google.com/) থেকে একটি সম্পূর্ণ ফ্রি API Key সংগ্রহ করুন।
2. আপনার GitHub রিপোজিটরির **Settings > Secrets and variables > Actions** এ যান।
3. **New repository secret** বাটনে ক্লিক করুন:
   - **Name:** `GEMINI_API_KEY`
   - **Secret:** আপনার কপি করা Gemini API Key টি পেস্ট করুন।
4. **Add secret** সংরক্ষণ করুন।

---

## ⚙️ কাস্টমাইজেশন (Customization):

`_config.yml` ফাইলটি খুলে আপনার পছন্দমত তথ্য পরিবর্তন করুন:
- **title:** আপনার ওয়েবসাইটের নাম।
- **telegram:** আপনার টেলিগ্রাম চ্যানেলের লিংক।
- **whatsapp:** আপনার হোয়াটসঅ্যাপ গ্রুপের লিংক।
- **url / baseurl:** আপনার GitHub Pages বা কাস্টম ডোমেনের ঠিকানা।

---

## 🤖 স্বয়ংক্রিয় কাজের রূপরেখা (How Automation Works):
```
[WBPSC / WBPRB / SSC / Employment News]
                  │
                  ▼
[GitHub Actions (.github/workflows/daily_job_bot.yml)]
                  │
                  ├─► scripts/runner.py
                  ├─► scrapers/* (নতুন নোটিফিকেশন চেক করে)
                  ├─► gemini_formatter.py (বাংলায় আর্টিকেল তৈরি করে)
                  └─► _posts/ ফোল্ডারে Markdown ফাইল তৈরি করে গিটহাবে পুশ করে
```

---

## 🧪 লোকাল টেস্ট (Local Testing):
আপনার কম্পিউটারে ম্যানুয়ালি টেস্ট করতে চাইলে:
```bash
pip install -r requirements.txt
python scripts/runner.py
```
নতুন পোস্ট তৈরি হয়ে সরাসরি `_posts/` ফোল্ডারে যুক্ত হবে।
